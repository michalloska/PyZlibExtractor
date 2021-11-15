#!/usr/bin/python3
# Michal Loska 08.11.2021
import argparse
import os.path
from datetime import datetime
import logging
import os

parser = argparse.ArgumentParser(
    usage="%(prog)s [options] [--min <number>] [--max <number>]",
    description="Uncompress multiple zlib files into a single output file. Archive names are log_archive.X.zlib, where X is a numer.",
)
parser.add_argument(
    "--max", "--max_archive_index", type=int, default=2, help="Index of the last file, default = 2 meaning single input archive"
)
parser.add_argument(
    "--min", "--min_archive_index", type=int, default=1, help="Index of the first file"
)
parser.add_argument(
    "--path",
    "--archives_path",
    type=str,
    default="./",
    help="Path to the archives directory. Uses CWD by default",
)
parser.add_argument(
    "--txt_log",
    "--txt_log_format",
    action="store_true",
    help="Use to save output logs into a .txt file. Default is .log",
)
parser.add_argument(
    "--rm",
    "--delete_zlibs",
    action="store_true",
    help="Delete the archives after uncompressing",
)
parser.add_argument(
    "--input_name",
    type=str,
    default="log_archive",
    help="Iutput file name (without format specifier)",
)
parser.add_argument(
    "--output_name",
    type=str,
    default="extracted_logs",
    help="Output file name (without format specifier)",
)
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logs")
_args = parser.parse_args()


_archive_name = _args.input_name
_archive_format = "zlib"
_uncompress_cmd = "zlib-flate"
_uncompress_cmd_flag = "-uncompress"
_processing_dir = _args.path if _args.path[-1] == "/" else _args.path + "/"
_output_log_format = ".log" if _args.txt_log == False else ".txt"
_output_compression_file_name = _args.output_name
_output_compression_file_path = (
    _processing_dir + _output_compression_file_name + _output_log_format
)


def uncompress_single_archive(archive_index, output_file):
    archive_name = f"{_archive_name}.{archive_index}.{_archive_format}"
    logs_divider_line = f"-------------- {archive_name} --------------"
    logs_divider_line_cmd = f"echo {logs_divider_line} >> {output_file}"

    os.system(logs_divider_line_cmd)
    cmd = f"{_uncompress_cmd} {_uncompress_cmd_flag} < {_processing_dir}{archive_name} >> {output_file}"
    logging.debug(
        f"Command parameters:\n archive_index = {archive_index},\n output_file = {output_file},\n archive_name = {archive_name},\n cmd = {cmd},\n logs_divider_line_cmd = {logs_divider_line_cmd}"
    )
    output = os.system(cmd)
    logging.info(f"Uncompressed {archive_index} archive to {output_file}")


def delete_single_archive(archive_index):
    archive_path = f"{_processing_dir}{_archive_name}.{archive_index}.{_archive_format}"
    os.remove(archive_path)
    logging.info(f"Removed archive = {archive_path}\n")


def is_default_output_file_present():
    return os.path.exists(_output_compression_file_path)


def get_new_output_file_name():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    chopped_file_name = _output_compression_file_path.rsplit(".", 1)
    return chopped_file_name[0] + "_" + current_time + "." + chopped_file_name[1]


def create_output_file(file_name):
    file = open(file_name, "a")
    file.close()


if __name__ == "__main__":
    if _args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    logging.debug(f"Using archives path: {_processing_dir}")
    logging.debug(f"User Arguments: {vars(_args)}")

    output_file_name = _output_compression_file_path
    if is_default_output_file_present():
        logging.info("default output file is already present, creating a new file")
        output_file_name = get_new_output_file_name()

    create_output_file(output_file_name)

    for_loop_step = -1
    remove_archives_after_uncompressing = _args.rm
    for archive_index in range(_args.max, _args.min - 1, for_loop_step):
        uncompress_single_archive(archive_index, output_file_name)
        if(remove_archives_after_uncompressing):
            delete_single_archive(archive_index)

    logging.info(f"Uncompressed total of {_args.max} archives to {output_file_name}")
