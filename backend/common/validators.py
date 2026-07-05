from rest_framework import serializers
ALLOWED_IMAGE_MIME_TYPES={'image/jpeg','image/png','image/webp'}
def require_cloudinary_url(value):
    if value and 'res.cloudinary.com' not in value:
        raise serializers.ValidationError('Images must be uploaded to Cloudinary and stored as a secure URL.')
    return value
