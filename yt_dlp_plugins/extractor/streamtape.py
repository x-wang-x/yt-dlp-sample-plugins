import re

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import urljoin


class StreamtapeIE(InfoExtractor):
    IE_NAME = 'streamtape'
    _VALID_URL = r'https?://(?:www\.)?(?P<host>(?:streamtape|advertape|strcloud|shavetape|stape|maptape|strclouad)\.[a-z0-9]+)/(?:e|v)/(?P<id>[a-zA-Z0-9]+)'
    _TESTS = [{
        'url': 'https://streamtape.com/v/jVK9L2qGBrIq1J',
        'md5': '05cc034b4ae179f16059339be5ad26f1',
        'info_dict': {
            'id': 'jVK9L2qGBrIq1J',
            'ext': 'mp4',
            'title': 'OF - Emiri Momota & June Liu Shares Her BFs Cock XXX 1080p PERVYVIDEOS.COM',
            'thumbnail': r're:^https?://.*\.jpg$',
        },
    }]
    def _real_extract(self, url):
        m = self._match_valid_url(url)
        video_id = m.group('id')
        host = m.group('host')

        webpage_url = f'https://{host}/v/{video_id}'
        webpage = self._download_webpage(webpage_url, video_id)

        token = self._search_regex(
            r"document\.getElementById\(['\"]norobotlink['\"]\)\.innerHTML\s*=\s*['\"].*?token=([^'\"]+)['\"]",
            webpage, 'token',
        )
        raw = self._search_regex(
            r'<div[^>]+id=["\']ideoooolink["\'][^>]*>(.*?)</div>',
            webpage, 'ideoooolink', flags=re.DOTALL,
        )
        clean = re.sub(r'<[^>]+>', '', raw).strip()
        final_url = f'https:/{clean}&token={token}&dl=1'
        title = self._og_search_title(webpage, default=video_id)
        title = re.sub(r'\.(mp4|mkv|webm)$', '', title, flags=re.I)

        poster = self._html_search_regex(r' id="mainvideo"[^>]* poster="(?P<data>.*?)"',
                                         webpage, 'poster', group='data')
        poster = urljoin(url, poster)


        return {
            'id': video_id,
            'title': title,
            'thumbnail': poster,
            'url': final_url,
            'ext': 'mp4',
        }
