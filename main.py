import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
# import wx
import glob
import re

NameFile = 'new_name.dxf'


def name_file(method_fixing, type_template, size_a, size_b, dist, ind_diam, ind_num):
    # TODO: Тип трафарета:
    #   Необходимо понять, будет это одна функция для всех
    #   или для каждого типа своя функция
    if size_a < size_b:
        size_a, size_b = size_b, size_a
    NameFile = str(f'{method_fixing} К{ind_diam}.{type_template}.{size_a}_{size_b}.{dist}')
    return NameFile


def create_dfx(NameFile, dist=60, rad_ind=35 / 2, n_ind=10):
    """
    Создание чертежа трафарета в формате dxf по заданным параметрам:
    :param NameFile: Имя файла для сохранения
    :param dist: Расстояние между индикаторами
    :param rad_ind: Радиус индикатора
    :param n_ind: Количество индикаторов
    :return: None
    """

    # создаем документ:
    doc = ezdxf.new()
    # обращаемся к пространству модели:
    msp = doc.modelspace()
    # psp = doc.layout('list1')

    for i in range(n_ind):
        for j in range(n_ind):
            msp.add_circle((i * dist, j * dist), radius=rad_ind)
    p1 = (0, 0)
    p2 = ((n_ind - 1) * dist, 0)

    dim = msp.add_aligned_dim(p1=p1, p2=p2, distance=-100, override={'dimtxt': 20})
    dim.render()
    doc.saveas(NameFile)


class DXF2IMG(object):
    default_img_format = '.pdf'
    default_img_res = 300

    def convert_dxf2img(self,
                        names,
                        img_format=default_img_format,
                        img_res=default_img_res):
        for name in names:
            doc = ezdxf.readfile(name)  # Открываем файл .dxf
            msp = doc.modelspace()  # получаем
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                raise Exception("The DXF document is damaged and can't be converted!")
            else:
                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                ctx = RenderContext(doc)
                ctx.set_current_layout(msp)
                ctx.current_layout.set_colors(bg='#FFFFFF')
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(msp, finalize=True)

                img_name = re.findall("(\S+)\.", name)  # select the image name that is the same as the dxf file name
                first_param = ''.join(img_name) + img_format  # concatenate list and string
                fig.savefig(first_param, dpi=img_res)


if __name__ == '__main__':
    create_dfx(NameFile)
    first = DXF2IMG()
    first.convert_dxf2img([NameFile], img_format='.pdf')
