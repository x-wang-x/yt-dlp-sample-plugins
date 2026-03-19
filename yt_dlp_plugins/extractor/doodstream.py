import random
import string
import time

from yt_dlp.extractor.common import InfoExtractor


class DoodStreamIE(InfoExtractor):
    IE_NAME = 'doodstream'
    _VALID_URL = r'https?://(?:www\.)?(?P<host>dood\.(?:to|la|li|pm|re|sh|watch|ws|one)|ds2play\.com|dsvplay\.com|myvidplay\.com)/[ed]/(?P<id>[a-z\d]+)'
    _TESTS = [{
        'url': 'https://dood.so/d/jzrxn12t2s7n',
        'only_matching': True
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        url = f'https://dood.to/e/{video_id}'
        webpage = self._download_webpage(url, video_id)

        title = self._html_search_meta(
            ('og:title', 'twitter:title'), webpage, default=None) or self._html_extract_title(webpage)
        thumb = self._html_search_meta(['og:image', 'twitter:image'], webpage, default=None)
        token = self._html_search_regex(r'[?&]token=([a-z0-9]+)[&\']', webpage, 'token')
        description = self._html_search_meta(
            ['og:description', 'description', 'twitter:description'], webpage, default=None)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0',
            'referer': url,
        }

        pass_md5 = self._html_search_regex(r'(/pass_md5.*?)\'', webpage, 'pass_md5')
        final_url = ''.join((
            self._download_webpage(f'https://dood.to{pass_md5}', video_id, headers=headers),
            *(random.choice(string.ascii_letters + string.digits) for _ in range(10)),
            f'?token={token}&expiry={int(time.time() * 1000)}',
        ))

        return {
            'id': video_id,
            'title': title,
            'url': final_url,
            'http_headers': headers,
            'ext': 'mp4',
            'description': description,
            'thumbnail': thumb,
        }
