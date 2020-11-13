import requests
import pygal
from pygal.style import LightSolarizedStyle as LCS, LightStyle as LS

# 执行API调用并存储响应
language = "python"
url = "https://api.github.com/search/repositories?q=language:{}&sort=star".format(
    language)
r = requests.get(url)
print("Status code:", r.status_code)

# 将API响应存储在一个变量中
response_dict = r.json()
print("Total respositories:", response_dict['total_count'])
# 研究有关仓库的信息
repo_dicts = response_dict['items']
print("Number of items:", len(repo_dicts))

# 可视化
# my_style = LS('#333366', base_style=LCS)
my_style = LCS

my_config = pygal.Config()  # 实例化配置文件
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

# names, stars = [], []
# for repo_dict in repo_dicts:
#     names.append(repo_dict['name'])
#     stars.append(repo_dict['stargazers_count'])
names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    plot_dict = {
        'value': repo_dict['stargazers_count'],# y坐标的值
        'label': repo_dict['description'],# 标签内容
        'xlink':repo_dict['html_url']# 超链接
    }
    plot_dicts.append(plot_dict)

chart = pygal.Bar(my_config, style=my_style)
chart.title = "Most-Starred {} Projects on Github".format(
    language.capitalize())
chart.x_labels = names
# chart.add('', stars)
chart.add('',plot_dicts)

chart.render_to_file('{}_repos.svg'.format(language))
