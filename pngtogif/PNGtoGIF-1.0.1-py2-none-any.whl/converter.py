
import glob
from PIL import Image

class GifConverter:
    def __init__(self,path_in=None, path_out=None, resize=(320,240)):
        """
        path_in : 원본 여러 이미지 경로(ex: images/*.png)
        path_out : 결과 이미지 경로(ex: output/filename.gif)
        resize: 리사이징 크기(ex: (320,240))
        """
        # 사용자가 따로 설정하지 않으면 예외처리
        self.path_in = path_in or './*.png'
        self.path_out = path_out or './output.gif'
        self.resize = resize

    def convert_gif(self):
        """
        GIF 이미지 변환 기능 수행
        """
        img, *images = \
        [Image.open(f).resize(self.resize, Image.ANTIALIAS) for f in sorted(glob.glob(self.path_in))]

        try:
            img.save(
                fp=self.path_out,
                format='GIF',
                append_images = images,
                save_all=True,
                duration = 500,
                loop = 0
            )                    
        except IOError:
            print('Cannot Convert', img)


if __name__ == '__main__':
    # 클래스 테스트
    c = GifConverter('./project/images/*.png', './project/image_out/result.gif',(320,240))

    # 변환
    c.convert_gif()