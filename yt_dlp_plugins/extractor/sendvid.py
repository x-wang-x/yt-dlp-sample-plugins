import re

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import url_or_none


class SendvidIE(InfoExtractor):
    IE_NAME = "sendvid"
    _VALID_URL = (
        r"https?://(?:www\.)?sendvid\.com/(?:embed/)?(?P<id>[a-zA-Z0-9]+)(?:[/?#]|$)"
    )
    _TESTS = [
        {
            "url": "https://sendvid.com/3lja82fg",
            "info_dict": {
                "id": "3lja82fg",
                "ext": "mp4",
                "title": "juanita vargas new vid",
                "thumbnail": r"re:^https?://.*\.jpg$",
                "description": r"re:Upload and share videos instantly",
            },
        },
        {
            "url": "https://sendvid.com/embed/3lja82fg",
            "only_matching": True,
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # Download webpage with referer header
        headers = {
            "Referer": url,
        }
        webpage = self._download_webpage(url, video_id, headers=headers)

        # Extract title
        title = self._html_search_meta("og:title", webpage, default=None)
        if not title:
            title = self._html_search_regex(
                r"<title>([^<]+)</title>", webpage, "title", default=None
            )
        if not title:
            title = video_id

        # Extract video URL
        video_url = self._html_search_meta("og:video", webpage, default=None)
        if not video_url:
            video_url = self._search_regex(
                r'<source[^>]+id=["\']video_source["\'][^>]+src=["\']([^"\']+)',
                webpage,
                "video_url",
            )
        video_url = url_or_none(video_url)

        # Extract thumbnail
        thumbnail = self._html_search_meta("og:image", webpage, default=None)

        # Extract description
        description = self._html_search_meta(
            ("og:description", "description"), webpage, default=None
        )

        return {
            "id": video_id,
            "title": title,
            "url": video_url,
            "thumbnail": thumbnail,
            "description": description,
            "http_headers": headers,
            "ext": "mp4",
        }
