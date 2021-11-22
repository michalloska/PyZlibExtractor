#!/usr/bin/python3
# Michal Loska 22.11.2021
import argparse
import os.path
from datetime import datetime
import logging
import os
import json
import pprint

logging.basicConfig(
    format="[%(levelname)s] - %(asctime)s - [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%H:%M",
)

parser = argparse.ArgumentParser(
    usage="%(prog)s [options] [--min <number>] [--max <number>]",
    description="Uncompress multiple zlib files into a single output file. Archive names are log_archive.X.zlib, where X is a numer.",
)
parser.add_argument(
    "--max",
    "--max_archive_index",
    type=int,
    help="Index of the last file, when unspecified single archive extraction is assumed",
)
parser.add_argument(
    "--min",
    "--min_archive_index",
    type=int,
    help="Index of the first file, when unspecified single archive extraction is assumed",
)
parser.add_argument(
    "--path",
    "--archives_path",
    type=str,
    default="./",
    help="Path to the archives directory. Output will be generated in this path too. Uses CWD by default",
)
parser.add_argument(
    "--txt_log_format",
    action="store_true",
    help="Use .txt format for output logs. Default is .log. This setting can be overwritten in '--output_name'",
)
parser.add_argument(
    "--rm",
    "--delete_archives",
    action="store_true",
    help="Delete the archives after uncompressing",
)
parser.add_argument(
    "--input_name",
    type=str,
    help="Input file name (with or without format specifier)",
)
parser.add_argument(
    "--output_name",
    type=str,
    default="extracted_logs",
    help="Output file name (when format specified it will overwrite '--txt_log_format')",
)
parser.add_argument(
    "-s",
    "--save_preset",
    action="store_true",
    help="Save current arguments as a .preset.json file under /tmp/PyZlibExtractor/. Can be used when --load_preset specified",
)
parser.add_argument(
    "--load_preset",
    action="store_true",
    help="Use previously set preset. Will be used automatically next time",
)
parser.add_argument(
    "--show_preset",
    action="store_true",
    help="Display preset",
)
parser.add_argument(
    "--delete_preset",
    action="store_true",
    help="Delete preset file",
)
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logs")
_args = parser.parse_args()
_args_defaults = parser.parse_args([])

_app_config_dir = "/tmp/PyZlibExtractor/"
_arguments_preset_json_file = os.path.join(_app_config_dir, ".preset.json")
_archive_format = "zlib"
_uncompress_cmd = "zlib-flate -uncompress"
_processing_dir = _args.path if _args.path[-1] == "/" else _args.path + "/"
_supported_log_formats = {"txt": ".txt", "log": ".log"}
_output_log_format = (
    _supported_log_formats["log"]
    if _args.txt_log_format == False
    else _supported_log_formats["txt"]
)
_output_compression_file_name = _args.output_name
_output_compression_file_path = (
    _processing_dir + _output_compression_file_name + _output_log_format
)
_not_overwritable_keys = [
    "save_preset",
    "load_preset",
    "show_preset",
    "debug",
]


def validate_input_arguments(input_arguments):
    # path
    if not os.path.exists(input_arguments["path"]):
        logging.critical(
            f"The specified path {input_arguments['path']} does not exist! Quitting!"
        )
        exit()

    # input_name
    if input_arguments["input_name"] is not None:
        input_name_split = input_arguments["input_name"].rsplit(".", 1)
        if len(input_name_split) != 1:
            input_archive_format = input_name_split[1]
            if input_archive_format != _archive_format:
                logging.critical(
                    f"This script does not support {input_archive_format} file format! Quitting!"
                )
                exit()
            input_arguments["input_name"] = input_name_split[0]
            logging.debug(
                f"input_name was specified with format, ditching format specifier and continuing with name = {input_arguments['input_name']}"
            )

    # output_name
    output_name_split = input_arguments["output_name"].rsplit(".", 1)
    if len(output_name_split) != 1:
        output_file_format = output_name_split[1]
        if output_file_format not in _supported_log_formats.keys():
            logging.critical(
                f"This script does not support '{output_file_format}' output file format! Quitting!"
            )
            exit()

        global _output_compression_file_name
        global _output_log_format
        global _output_compression_file_path
        
        _output_compression_file_name = output_name_split[0]
        _output_log_format = _supported_log_formats[output_file_format]
        _output_compression_file_path = _processing_dir + _output_compression_file_name + _output_log_format
        logging.debug(
            f"Overriding output log file format to: {_output_log_format} based on the '--output_name' param"
        )


def save_arguments_preset_to_json(input_arguments):
    os.makedirs(os.path.dirname(_app_config_dir), exist_ok=True)
    with open(_arguments_preset_json_file, "w") as preset_file:
        json.dump(vars(input_arguments), preset_file)
        logging.info(
            f"Saved arguments as a preset to file: {os.path.realpath(preset_file.name)}"
        )


def load_arguments_preset_from_json():
    with open(_arguments_preset_json_file, "r") as preset_file:
        user_arguments = json.load(preset_file)
        logging.info(
            f"Loaded arguments from a preset: {os.path.realpath(preset_file.name)}"
        )
        return user_arguments


def display_preset():
    try:
        with open(_arguments_preset_json_file, "r") as preset_file:
            user_arguments = json.load(preset_file)
            logging.info("Displaying saved preset:\n")
            pprint.pprint(user_arguments)
    except FileNotFoundError as error:
        logging.critical(f"Preset file does not exist!")
        exit()


def delete_preset():
    try:
        os.remove(_arguments_preset_json_file)
        logging.info(f"Removed preset file: {_arguments_preset_json_file}\n")
    except FileNotFoundError as error:
        logging.critical(f"Preset file cannot be deleted because it does not exist!")
        exit()
    except Exception as error:
        logging.critical(f"Exception was thrown while deleting preset file: {error}")
        exit()


def uncompress_single_archive(archive_name, output_file):
    logs_divider_line = f"-------------- {archive_name} --------------"
    logs_divider_line_cmd = f"echo {logs_divider_line} >> {output_file}"

    os.system(logs_divider_line_cmd)
    cmd = f"{_uncompress_cmd} < {_processing_dir}{archive_name} >> {output_file}"
    logging.debug(
        f"Command parameters:\n output_file = {output_file},\n archive_name = {archive_name},\n cmd = {cmd},\n logs_divider_line_cmd = {logs_divider_line_cmd}"
    )
    output = os.system(cmd)
    if output != 0:
        logging.critical(
            f"{_processing_dir}{archive_name} archive does not exist! Quitting..."
        )
        exit()
    logging.info(f"Successfully uncompressed {archive_name} archive to {output_file}")


def delete_single_archive(archive_name):
    archive_path = f"{_processing_dir}{archive_name}"
    output = os.remove(archive_path)
    logging.info(f"Removed archive = {archive_path} with output status = {output}\n")


def is_default_output_file_present():
    return os.path.exists(_output_compression_file_path)


def get_new_output_file_name():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    chopped_file_name = _output_compression_file_path.rsplit(".", 1)
    return chopped_file_name[0] + "_" + current_time + "." + chopped_file_name[1]


def prepare_output_file():
    output_file_name = _output_compression_file_path
    if is_default_output_file_present():
        logging.info("Output file is already present, creating a new file")
        output_file_name = get_new_output_file_name()
    create_output_file(output_file_name)
    return output_file_name


def create_output_file(file_name):
    file = open(file_name, "a")
    file.close()


def get_archive_name_for_single_input_archive(user_arguments):
    return f"{user_arguments['input_name']}.{_archive_format}"


def get_archive_name_for_multiple_input_archive(user_arguments, archive_index):
    return f"{user_arguments['input_name']}.{archive_index}.{_archive_format}"


def process_single_archive(user_arguments):
    archive_name = get_archive_name_for_single_input_archive(user_arguments)
    remove_archives_after_uncompressing = user_arguments["rm"]
    uncompress_single_archive(archive_name, output_file_name)
    if remove_archives_after_uncompressing:
        delete_single_archive(archive_name)


def process_multiple_archives(user_arguments):
    for_loop_step = -1
    remove_archives_after_uncompressing = user_arguments["rm"]
    for archive_index in range(
        user_arguments["max"], user_arguments["min"] - 1, for_loop_step
    ):
        archive_name = get_archive_name_for_multiple_input_archive(
            user_arguments, archive_index
        )
        uncompress_single_archive(archive_name, output_file_name)
        if remove_archives_after_uncompressing:
            delete_single_archive(archive_name)


if __name__ == "__main__":
    overwritten_arguments = {
        k: v
        for k, v in vars(_args).items()
        if vars(_args_defaults)[k] != vars(_args)[k] and k not in _not_overwritable_keys
    }
    user_arguments = vars(_args)

    if user_arguments["debug"]:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    validate_input_arguments(user_arguments)
    should_save_preset = user_arguments["save_preset"]
    should_load_preset = user_arguments["load_preset"]
    should_show_preset = user_arguments["show_preset"]
    should_delete_preset = user_arguments["delete_preset"]

    if should_show_preset:
        display_preset()
        exit()

    if should_delete_preset:
        delete_preset()
        exit()

    if should_load_preset:
        try:
            user_arguments = load_arguments_preset_from_json()

            user_arguments.update(overwritten_arguments)
            logging.info(
                f"Updated the preset values with cli arguments: {overwritten_arguments}"
            )

            if user_arguments["debug"]:
                logging.getLogger().setLevel(logging.DEBUG)

        except FileNotFoundError as error:
            logging.critical(
                f"Required arguments not present and {_arguments_preset_json_file} file does not exist! Set the required parameters to proceed. Quitting..."
            )
            exit()
    elif _args.input_name is None:
        logging.critical(
            f"Required arguments not present! Set the required parameters to proceed. Quitting..."
        )
        exit()

    if should_save_preset:
        save_arguments_preset_to_json(_args)

    logging.debug(f"User Arguments: {user_arguments}")

    output_file_name = prepare_output_file()
    if user_arguments["min"] is None or user_arguments["max"] is None:
        process_single_archive(user_arguments)
    else:
        process_multiple_archives(user_arguments)

    logging.info(
        f"Successfully uncompressed total of {user_arguments['max']} archives to {os.path.realpath(output_file_name)}"
    )
