import argparse
import os
from os.path import join
from urllib.parse import urlparse

from url_scraper import UrlScraper
from utils.general import replace_slashes_with_dashes, get_url_variations
from bfs_node import BfsNode


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--link', type=str, help='Link from which we should start scraping images')
    parser.add_argument('--target-folder', type=str, help='Path to the folder for saving images')
    parser.add_argument('--depth', type=str, help='Traversing depth')
    parser.add_argument('--min-height', type=int, help='Minimal height of images we should save')
    parser.add_argument('--min-width', type=int, help='Minimal width of images we should save')

    args = parser.parse_args()

    if not os.path.exists(args.target_folder):
        os.makedirs(args.target_folder)

    visited, queue = set(), [BfsNode(url=args.link, output_folder=args.target_folder, depth=0)]
    while queue:
        cur_url, cur_dir, cur_depth = queue.pop(0)
        cur_url_scrapper = UrlScraper(cur_url)
        if cur_url in visited:
            continue
        if not os.path.exists(cur_dir):
            os.makedirs(cur_dir)
        cur_url_scrapper.save_all_images(output_folder=cur_dir, min_width=args.min_width, min_height=args.min_height)
        visited.add(cur_url)

        if cur_depth == args.depth:
            continue
        links_with_same_domain = cur_url_scrapper.get_links_with_same_domain()

        for neighbour_url in links_with_same_domain:
            neighbour_url_variations = get_url_variations(neighbour_url)
            if any(u in visited for u in neighbour_url_variations):
                continue
            neighbour_url_parsed = urlparse(neighbour_url)
            neighbour_dir = join(
                cur_dir,
                replace_slashes_with_dashes(neighbour_url_parsed.netloc) +
                replace_slashes_with_dashes(neighbour_url_parsed.path)
            )
            queue.append(BfsNode(url=neighbour_url, output_folder=neighbour_dir, depth=cur_depth+1))


if __name__ == '__main__':
    main()
