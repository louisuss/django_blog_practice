import os
from PIL import Image  # 이미지 처리 라이브러리
from django.db.models.fields.files import ImageField, ImageFieldFile


# 커스텀 필드 작성 시 기존의 비슷한 필드를 상속받아 작성하는 것이 보통
# -> 이미지 관련 커스텀 필드는 ImageField 상속받음
# ImageField는 이미지 파일을 파일 시스템에 쓰고 삭제하는 작업이 필요, 추가적으로 ImageFieldFile 필요. 두 클래스 연계 코드 필요

# 파일 시스템에 직접 파일을 쓰고 지우는 작업
class ThumbnailImageFieldFile(ImageFieldFile):
    # 기존 이미지 파일명 기준으로 썸네일 이미지 파일명 만듬
    # 썸네일 이미지 경로나 URL 만들 때 사용
    # ex) abc.jpg -> abc.thumb.jpg
    def _add_thumb(self, s):
        parts = s.split(".")
        parts.insert(-1, "thumb")
        if parts[-1].lower() not in ['jpeg', 'jpg']:
            parts[-1] = 'jpg'
        return ".".join(parts)

    # 원본 파일의 경로인 path 속성에 추가해, 썸네일의 경로인 thumb_path 속성 만듬
    @property  # 메소드를 멤버 변수처럼 사용 가능
    def thumb_path(self):
        return self._add_thumb(self.path)

    # 원본 파일의 URL인 url 속성에 추가해, 썸네일의 URL인 thumb_url 속성 만듬
    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    # 파일 시스템에 파일 저장 및 생성
    def save(self, name, content, save=True):
        # 부모 ImageFieldFile 클래스의 save() 메소드 호출해 원본 이미지 저장
        super().save(name, content, save)

        img = Image.open(self.path)

        # 원본 파일로부터 디폴트 128X128 크기 썸네일 이미지 생성
        size = (self.field.thumb_width, self.field.thumb_height)
        # PIL 라이브러리 Image.thumbnail() 함수. 썸네일 이미지 만듬. 썸네일 만들 때 원본 이미지의 가로, 세로 비율 유지
        img.thumbnail(size)

        # RGB 모드인 동일한 크기의 백그라운드 이미지 생성
        background = Image.new('RGB', size, (255, 255, 255))
        # 썸네일과 백그라운드 이미지 합쳐 정사각형 모양의 썸네일 이미지 생성. 정사각형 빈공간은 백그라운드 이미지에 의해 흰색 처리
        box = (int((size[0] - img.size[0])/2), int((size[1] - img.size[1])/2))
        background.paste(img, box)
        # 합쳐진 최종 이미지를 JPEG 형식으로 파일 시스템의 thumb_path 경로에 저장
        background.save(self.thumb_path, 'JPEG')

    # 원본 이미지 및 썸네일 이미지도 같이 삭제
    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)

# 장고 모델 정의에 사용하는 필드 역할


class ThumbnailImageField(ImageField):
    # ThumbnailImageField와 같은 새로운 FileField 클래스 정의할 때는 그에 상응하는 File 처리 클래스를 attr_class 속성에 지정하는 것이 필수
    # ThumbnailImageField에 상응하는 File 클래스로  ThumbnailImageFieldFile 지정
    attr_class = ThumbnailImageFieldFile

    def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs):
        # 필드 정의 시 크기 옵션 조정
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        # 부모 ImageField 클래스의 생성자 호출해 관련 속성들 초기화
        super().__init__(verbose_name, **kwargs)
