import glob
from PIL import Image

class GifConverter:
    def __init__(self, path_in=None, path_out=None, resize=(320, 240)):
        '''
        path_in : 원본 여러 이미지 경로 (Ex:images/*.png)
        path_out : 결과 이미지 경로 (Ex : output/filename.gif)
        resize : 리사이징 크기 (320,240)
        '''
        self.path_in = path_in or './*.png'  # 현재 경로에서 png가 있는 곳에서 실행하기(예외발생 방지)
        self.path_out = path_out or './output.gif'
        self.resize = resize

    def convert_gif(self):
        '''
        GIF 이미지 변환 기능 수행
        '''
        img, *images = \
            [Image.open(f).resize(self.resize, Image.ANTIALIAS) for f in sorted(glob.glob(self.path_in))]

        try:
            img.save(
                fp=self.path_out,
                format='GIF',
                append_images=images,
                save_all=True,
                duration=500,  # 크기가 클 수록 화면 전환 속도가 느려짐
                loop=0
            )
        except IOError:
            print('Cannot convert', img)


if __name__ == "__main__":
    # 클래스
    c = GifConverter('../section4/image/*.jpg', '../section4/image_out/result.gif', (320, 240))

    # 변환
    c.convert_gif()
