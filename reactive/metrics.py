import yaml
import os
from subprocess import check_output, check_call, CalledProcessError

from charms.reactive import hook
from charms.metrics import add_metric


def collect_metrics(doc):
    values = {}
    metrics = doc.get("metrics", {})
    for metric, mdoc in metrics.items():
        cmd = mdoc.get("command")
        if cmd:
            try:
                value = check_output(cmd, shell=True, universal_newlines=True)
            except CalledProcessError as e:
                check_call(['juju-log', '-lERROR',
                            'Error collecting metric {}:\n{}'.format(
                                metric, e.output)])
                continue
            value = value.strip()
            if value:
                values[metric] = value

    if not values:
        return

    add_metric(values**)


@hook('collect-metrics')
def collect():
    charm_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
    metrics_yaml = os.path.join(charm_dir, "metrics.yaml")
    with open(metrics_yaml) as f:
        doc = yaml.load(f)
        collect_metrics(doc)
