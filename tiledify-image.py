# coding: utf-8

import os
import argparse
from os import path
from collections import namedtuple
from PIL import Image


args_parser = argparse.ArgumentParser()
args_parser.add_argument('input', type=str, help='input image (example: test.jpg)')
args_parser.add_argument('--row', type=int, default=5, help='row (default: 5)')
args_parser.add_argument('--column', type=int, default=5, help='column (default: 5)')

Point = namedtuple('Point', ['x', 'y'])
Tile = namedtuple('Tiled', ['point', 'width', 'height'])


def load_image(src_path):
    img = Image.open(src_path)  # type: Image.Image
    return img

def crop_tile_image(src_img, tile):
    box = (tile.point.x, tile.point.y, tile.point.x+tile.width, tile.point.y+tile.height)
    # print('box: {}'.format(box))
    tile_image = src_img.crop(box)
    return tile_image

def main():
    args = args_parser.parse_args()

    # 检查输入
    if not path.exists(args.input):
        print('tiledify-image: 输入文件不存在')
        return

    if args.row <= 0 or args.column <= 0:
        print('tiledify-image: 长度或者宽度输入有误')
        return

    # 获取磁块的数量
    tile_amount_on_x = args.row
    tile_amount_on_y = args.column

    # 获取图片大小信息
    input_image = load_image(args.input)
    input_image_size = (input_image.size[0], input_image.size[1])
    img_w, img_h = input_image_size
    print('tiledify-image: 图片的大小为 ({}, {})'.format(img_w, img_h))

    # 计算出瓷块的高宽
    tile_w = img_w / tile_amount_on_x
    tile_h = img_h / tile_amount_on_y

    if not tile_w or not tile_h:
        # TODO: 报错
        print('tiledify-image: 磁块的 长/宽 太小，尝试调整数量')
        return

    # 磁块列表
    tiles = []
    for y in range(tile_amount_on_y):
        for x in range(tile_amount_on_x):
            p = Point(x*tile_w, y*tile_h)
            tile = Tile(p, tile_w, tile_h)
            tiles.append(tile)

    # 裁剪出图片
    tile_images = []
    for tile in tiles:
        tile_image = crop_tile_image(input_image, tile)
        tile_images.append(tile_image)

    # 写入文件夹
    if not path.exists('output'):
        os.mkdir('output')

    for idx, tile_image in enumerate(tile_images, start=1):
        output_path = 'output/{}.jpg'.format(idx)
        tile_image.save(output_path, "JPEG")
        print('tiledify-image: 输出到 {} 成功 ({}/{})'.format(output_path, idx, len(tile_images)))

    # TODO: 打包成 zip
    pass
    


if __name__ == "__main__":
    main()
