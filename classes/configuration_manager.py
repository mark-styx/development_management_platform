from _conf import config
import argparse

conf = config()
commands = {
    'add_config':conf.add_configuration,
    'rem_config':conf.rem_configuration,
    'upd_config':conf.update_conf
}

if __name__ == "__main__":
    '''Command line tool to add, update, and remove configurations from the configuration dictionary.
    input:
        key_val: Optional, must be present if command is add/update; takes 2 args
        command: Command to execute; add_config, rem_config, upd_config
        category: The key to modify in the configuration dictionary
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command',help='add_config, rem_config, or upd_config'
        )
    parser.add_argument(
        'category',help='the key in the config dictionary to be affected'
        )
    parser.add_argument(
        '-kv','--key_val',nargs=2,help='the key value pair of the update or input',action='store'
        )
    args = parser.parse_args()
    if args.command in ['add_config','upd_config']:
        assert(args.key_val)
        payload = {args.category:{args.key_val[0]:args.key_val[1]}}
    if args.command == 'rem_config': payload = args.category
    commands[args.command](payload)