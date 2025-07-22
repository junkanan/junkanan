import sys
from typing import List

try:
    from youtubesearchpython import VideosSearch
except Exception as e:
    print("Failed to import youtube-search-python library:", e)
    print("Install with `pip install youtube-search-python`.")
    sys.exit(1)

try:
    from pytube import YouTube
except Exception as e:
    print("Failed to import pytube library:", e)
    print("Install with `pip install pytube`.")
    sys.exit(1)


def search_videos(query: str, limit: int = 10) -> List[dict]:
    """Search YouTube videos by query and return results."""
    videos_search = VideosSearch(query, limit=limit)
    results = videos_search.result().get("result", [])
    for idx, vid in enumerate(results, start=1):
        title = vid.get("title", "Unknown title")
        duration = vid.get("duration", "?")
        print(f"{idx}. {title} ({duration})")
    return results


def parse_selection(raw: str, total: int) -> List[int]:
    """Parse user selection string into a list of unique indices."""
    indices = set()
    for part in raw.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            idx = int(part)
        except ValueError:
            print(f"Invalid selection: {part}")
            continue
        if 1 <= idx <= total:
            indices.add(idx)
        else:
            print(f"Ignoring out-of-range index: {idx}")
    return sorted(indices)


def download_video(url: str, output_path: str = '.') -> None:
    """Download a YouTube video at the highest resolution."""
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        print(f"Downloading: {yt.title}")
        stream.download(output_path=output_path)
        print("Downloaded successfully.\n")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def main() -> None:
    query = ' '.join(sys.argv[1:])
    if not query:
        query = input("Enter search keywords: ").strip()
    if not query:
        print("No query provided.")
        return
    results = search_videos(query)
    if not results:
        print("No videos found.")
        return
    selection = input("Select videos to download (comma separated numbers): ")
    indices = parse_selection(selection, len(results))
    if not indices:
        print("No valid selection made.")
        return
    for idx in indices:
        url = results[idx - 1].get('link')
        if url:
            download_video(url)
        else:
            print(f"Missing URL for selected video #{idx}.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
