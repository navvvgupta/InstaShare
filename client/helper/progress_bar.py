# progress_bar.py
import sys
import tqdm


def main(filename, filesize, progress_pipe):
    filesize = int(filesize)
    progress = tqdm.tqdm(
        range(filesize),
        f"Receiving {filename}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )

    while True:
        data = progress_pipe.read()
        if data:
            bytes_downloaded = int(data)
            progress.n = bytes_downloaded
            progress.refresh()
        else:
            break


if __name__ == "__main__":
    filename = sys.argv[1]
    filesize = sys.argv[2]
    progress_pipe = sys.stdin
    main(filename, filesize, progress_pipe)
