import argparse
import asyncio
import os
import aiofiles
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


async def copy_file(file_path: Path, output_folder: Path):
    try:
        extension_folder = output_folder / \
            file_path.suffix[1:]
        extension_folder.mkdir(parents=True, exist_ok=True)
        destination_path = extension_folder / file_path.name

        async with aiofiles.open(file_path, 'rb') as src_file:
            async with aiofiles.open(destination_path, 'wb') as dst_file:
                await dst_file.write(await src_file.read())

        logging.info(f"Copy file {file_path} to {destination_path}")

    except Exception as e:
        logging.error(f"An error occurred while copying the file {
                      file_path}: {e}")


async def read_folder(source_folder: Path, output_folder: Path):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file_name in files:
            file_path = Path(root) / file_name
            task = asyncio.create_task(copy_file(file_path, output_folder))
            tasks.append(task)

    await asyncio.gather(*tasks)


async def main():
    parser = argparse.ArgumentParser(
        description="Asynchronous sorting of files by extension.")
    parser.add_argument("source_folder", type=str,
                        help="The path to the source folder with the files.")
    parser.add_argument("output_folder", type=str,
                        help="The path to the destination folder for sorting files.")

    args = parser.parse_args()
    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(
            "The specified output folder does not exist or is not a directory.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)
    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
