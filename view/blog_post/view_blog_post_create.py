from Chimera.view.album.view_album_create import album_create as create_album
from Chimera.view.blob.view_blob_upload import blob_upload as upload_blob
from Chimera.storage_url_suffixes import StorageURLSuffixes
from Chimera.settings import TIME_FORMAT
from Chimera.utils import model_to_dict
from django.http import HttpResponse
from Chimera.models import BlogPost
from Chimera.results import Result
from json import loads, dumps
from datetime import datetime
from base64 import b64encode


def blog_post_create(request, **kwargs):
    if (request and request.method == 'POST') or kwargs:
        if request and request.method == 'POST':
            body = loads(request.body)
        elif kwargs:
            body = kwargs
        else:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        author_id = body.get('author_id')
        title = body.get('title')
        short_description = body.get('short_description')
        long_description = body.get('long_description')
        image = body.get('image')

        if not author_id and title and short_description and long_description and image:
            response = Result.get_result_dump(Result.INVALID_PARAMETER)
            return HttpResponse(response, content_type='application/json')

        post_time = datetime.utcnow().strftime(TIME_FORMAT)

        album_create_kwargs = {'Please': 'Thank you', }  # Junk args to pass kwargs null check
        album = create_album(request=None, **album_create_kwargs)

        blog_post = BlogPost(
            album_id=album.id,
            author_id=author_id,
            title=title,
            short_description=short_description,
            long_description=long_description,
            post_time=post_time,
        )

        try:
            blog_post.save()
        except StandardError:
            response = Result.get_result_dump(Result.DATABASE_CANNOT_SAVE_BLOG_POST)
            return HttpResponse(response, content_type='application/json')

        blob_upload_kwargs = {
            'file': b64encode(image.read()),
            'album_id': str(blog_post.album_id),
            'url_suffix': StorageURLSuffixes.get_url_suffix(StorageURLSuffixes.SIREN_BLOG),
        }

        upload_blob(request=None, **blob_upload_kwargs)

        if kwargs:
            return blog_post

        response = {'blog_post': model_to_dict(blog_post)}
        Result.append_result(response, Result.SUCCESS)
        response = dumps(response)
        return HttpResponse(response, content_type='application/json')
    else:
        response = Result.get_result_dump(Result.POST_ONLY)
        return HttpResponse(response, content_type='application/json')
