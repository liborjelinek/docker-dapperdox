#!/usr/bin/env python3

# Converts YAML to JSON while keeping YAML ordering of object members. Expect 'swagger.json' in specified specdir.

import json
import os
from collections import OrderedDict

import sys
import yaml


class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """
    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                                                    'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                                                        node.start_mark, 'found unacceptable key (%s)' % exc,
                                                        key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

# Missing specdir in commandline arguments
if len(sys.argv) == 1:
    script_file = sys.argv[0]           # name of this script
    sys.exit("Not specified directory with swagger.json. Use as 'python3 {} /path/to/specdir/'.".format(script_file))

spec_dir = sys.argv[1]

# TODO: Find YAML/YML files of any name recursively
yamls = [os.path.join(spec_dir, 'swagger.yaml')]

for yaml_file in yamls:
    # produces foo.json from foo.yaml
    json_file = os.path.join(spec_dir, os.path.splitext(os.path.basename(yaml_file))[0] + '.json')
    with open(yaml_file, 'r') as input, open(json_file, 'w') as output:
        json.dump(yaml.load(input, Loader=OrderedDictYAMLLoader), output, indent=4)
        print('Converted {} to {}'.format(yaml_file, os.path.basename(json_file)))
