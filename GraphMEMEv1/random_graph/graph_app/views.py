import matplotlib
matplotlib.use('Agg')  # Используем рендеринг без GUI

import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings
from django.shortcuts import render

def index(request):
    # Генерация случайных данных
    x = np.linspace(0, 10, 100)
    y = np.random.uniform(-1, 1, 100)

    # Создание графика
    plt.figure()
    plt.plot(x, y)
    plt.title('MEME COIN')

    # Путь для сохранения графика
    graph_path = os.path.join(settings.STATICFILES_DIRS[0], 'graph_app/graph.png')
    plt.savefig(graph_path)
    plt.close()

    return render(request, 'graph_app/index.html')
