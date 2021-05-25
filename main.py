import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import os.path
# import wx
import glob
import re
import config


def name_file(atr: dict):
    """Из входящих параметров формирует имя файла"""
    if atr['size_a'] < atr['size_b']:
        atr['size_a'], atr['size_b'] = atr['size_b'], atr['size_a']
    name = str(f'{atr["method_fixing"]} '
               f'К{atr["ind_diam"]}.'
               f'{atr["type_template"]}.'
               f'{atr["size_a"]}_{atr["size_b"]}.'
               f'{atr["dist"]}')
    return name


def check_file(NameFile):
    """Проверка наличия файла"""
    if os.path.isfile(f'Files/DXF/{NameFile}.dxf'):
        return True
    else:
        return False


def create_dxf(atr: dict):
    """
    Создание чертежа трафарета в формате dxf по заданным параметрам
    """

    name = name_file(atr)

    # создаем документ:
    doc = ezdxf.new()
    # обращаемся к пространству модели:
    msp = doc.modelspace()
    # psp = doc.layout('list1')

    if atr['type_template'] == 'Л':
        count_a = atr['size_a'] // atr['dist'] + 1
        count_b = atr['size_b'] // atr['dist'] + 1
        for i in range(count_a):
            for j in range(count_b):
                msp.add_circle((i * atr['dist'], j * atr['dist']), radius=atr['ind_diam'] / 2)
        # p1 = (0, 0)
        # p2 = ((atr['ind_num'] - 1) * atr['dist'], 0)
        # dim = msp.add_aligned_dim(p1=p1, p2=p2, distance=-100, override={'dimtxt': 20})  # отрисовка размерной линии
        # dim.render()
        doc.saveas('Files/DXF/' + name+'.dxf')

    elif atr['type_template'] == 'Ш':
        a = atr['dist'] / 2**0.5
        count_a = int((atr['size_a']-20) // a + 1)
        count_b = int((atr['size_b']-20) // a + 1)
        for i in range(count_a):
            for j in range(count_b):
                if (i + j) % 2 == 0:
                    msp.add_circle((a*i, a*j), radius=atr['ind_diam'] / 2)
        doc.saveas('Files/DXF/' + name+'.dxf')


class DXF2IMG(object):
    default_img_format = '.pdf'
    default_img_res = 300

    def convert_dxf2img(self,
                        path,
                        name_file,
                        img_format=default_img_format,
                        img_res=default_img_res):
        name = path + name_file + '.dxf'
        doc = ezdxf.readfile(name)  # Открываем файл .dxf
        msp = doc.modelspace()  # получаем
        auditor = doc.audit()
        if len(auditor.errors) != 0:
            raise Exception("The DXF document is damaged and can't be converted!")
        else:
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            ctx = RenderContext(doc)
            ctx.set_current_layout(msp)
            ctx.current_layout.set_colors(bg='#FFFFFF')
            out = MatplotlibBackend(ax, params={"lineweight_scaling": 0})
            Frontend(ctx, out).draw_layout(msp, finalize=True)
            fig.savefig(f'Files/pdf/{name_file}.pdf', dpi=img_res)
            fig.savefig(f'Files/png/{name_file}.png', dpi=img_res)

if __name__ == '__main__':
    atr = config.atr

    name = name_file(atr)
    if check_file(name):
        print('Такой уже есть')
    else:
        create_dxf(atr)
        file = DXF2IMG()
        file.convert_dxf2img('Files/DXF/', name)

