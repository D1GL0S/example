import pyautogui
import keyboard
import time
import math
from plyer import notification


pyautogui.FAILSAFE = False
target_image = 'nickname.png'
other_target_images = 'loop.png'
lvlmax = '2277.png'
discord_icon = (150, 940) # 150, 940
discord_loop = (1055, 45) # 1055, 45
white_pixel = (925, 245) # 925, 245
osrs_icon = (100, 940) # 100, 940
ppl = 4
target_white = 'Loot.png'
color = (0, 255, 255,)



# Функция для проверки, является ли пиксель красным (rgb = 255, 0, 0)
def is_red_pixel(pixel):


    return pixel[0] < 10 and pixel[1] > 210 and pixel[2] > 245

def is_green_pixel(pixel):
    return pixel[0] < 15 and pixel[1] < 15 and pixel[2] > 245

# Функция для прохода по выбранной области и поиска красных пикселей
def find_red_pixels(top_left_x, top_left_y, bottom_right_x, bottom_right_y):
    screenshot = pyautogui.screenshot()
    image = screenshot.copy()
    width, height = image.size
    pixel_data = image.load()

    red_pixels = []

    for x in range(top_left_x, bottom_right_x + 1):
        for y in range(top_left_y, bottom_right_y + 1):
            pixel = pixel_data[x, y]
            if is_red_pixel(pixel):
                red_pixels.append((x, y))
            if is_green_pixel(pixel):
                green = 1

    return red_pixels

# Функция для вычисления расстояния между двумя точками
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Функция для создания массивов из близких пикселей
def create_arrays(red_pixels):
    arrays = []

    while red_pixels:
        current_pixel = red_pixels.pop(0)  # Берем первый пиксель из списка
        new_array = [current_pixel]

        # Используем другой список для хранения индексов пикселей, которые нужно добавить
        to_add = []

        for i, pixel in enumerate(red_pixels):
            # Проверяем расстояние между пикселями
            if any(distance(x, y, pixel[0], pixel[1]) <= 10 for x, y in new_array):
                new_array.append(pixel)
                to_add.append(i)

        # Добавляем элементы в new_array
        for idx in reversed(to_add):
            new_array.append(red_pixels.pop(idx))

        arrays.append(new_array)

    return arrays



# Функция для клика по массиву (с абсолютными координатами)
def click_array(array):
    # Если массив пустой, выходим из функции
    if not array:
        return

    # Вычисляем средние значения координат всех пикселей в массиве
    avg_x = sum(pixel[0] for pixel in array) // len(array)
    avg_y = sum(pixel[1] for pixel in array) // len(array)

    # Производим клик по средним
    pyautogui.moveTo(avg_x, avg_y, 0.3)
    pyautogui.rightClick(avg_x, avg_y)
    pyautogui.press('1')
    time.sleep(3)


# Функция для поиска и клика по второй картинке
def find_and_click_second_target(other_target_images, timeout=5, confidence=0.8):
    start_time = time.time()

    while time.time() - start_time < timeout:
        other_target_position = pyautogui.locateOnScreen(other_target_images, confidence=confidence)
        lvlmaxpos = pyautogui.locateOnScreen('2277.png', confidence=0.95)
        if lvlmaxpos:
            return False
            break
        if other_target_position and not lvlmaxpos:
        #if other_target_position: лвл макс
            other_target_x, other_target_y, _, _ = other_target_position
            pyautogui.moveTo(other_target_x + 150, other_target_y + 10, 0.3)
            pyautogui.doubleClick(other_target_x + 150, other_target_y + 10)
            pyautogui.click(other_target_x + 150, other_target_y + 10)
            time.sleep(0.2)  # Подождать полсекунды
            pyautogui.press('f1')
            time.sleep(0.2)  # Подождать полсекунды
            return True
        time.sleep(0.2)
    return False
# Функция для поиска и клика по картинке
def find_and_click_target(top_left_x, top_left_y, bottom_right_x, bottom_right_y, other_target_image, timeout=5, confidence=0.8):
    target_position = pyautogui.locateOnScreen(target_image, region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y), confidence=confidence)
    if target_position:
        target_x, target_y, _, _ = target_position
        pyautogui.moveTo(target_x + 10, target_y + 10, 0.3)
        pyautogui.click(target_x + 10, target_y + 10)
        time.sleep(0.2)
        if find_and_click_second_target(other_target_images, timeout):
            return True
    else:
        print("Первая картинка не найдена на экране.")
        return False

# Получение координат углов области
#input("Нажмите Enter, чтобы выбрать верхний левый угол...")
#print("Укажите левый верхний угол области.")
#top_left_x, top_left_y = pyautogui.position()
top_left_x, top_left_y = 15, 410

#input("Нажмите Enter, чтобы выбрать нижний правый угол...")
#print("Укажите правый нижний угол области.")

#bottom_right_x, bottom_right_y = pyautogui.position()
bottom_right_x, bottom_right_y = 525, 860
pyautogui.rightClick(525, 860)

processed_positions = []
pyautogui.screenshot()
time.sleep(1)

while True:
    green = 0
    red_pixels = find_red_pixels(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    arrays = create_arrays(red_pixels)

    if not arrays or len(arrays) > ppl or green == 1:
        pyautogui.hotkey('F4')



        keyboard.press_and_release('F4')
        print("смена мира")
        arrays = []
        processed_positions = []


        time.sleep(9)
    else:
        arrays_to_process = arrays.copy()

        for array in arrays_to_process:
            if array[0] in processed_positions:
                continue

            click_array(array)
            pyautogui.click(*osrs_icon)
            time.sleep(3)
            loot = pyautogui.locateOnScreen('Loot.png', confidence=0.95)
            if loot:
                # Действия, если обнаружен белый пиксель в радиусе
                notification.notify(
                    title='Уведомление',
                    message=f'Белый пиксель'
                            f''
                            f' обнаружен на координатах. Программа завершает работу.',
                    timeout=10
                )
                exit()
            else:
                time.sleep(0.2)
                pyautogui.click(*osrs_icon)
                pyautogui.rightClick(bottom_right_x, bottom_right_y)
        pyautogui.hotkey('F4')
        keyboard.press_and_release('F4')
        print("смена мира")
        arrays = []
        processed_positions = []
        time.sleep(11)


"""           if find_and_click_target(top_left_x, top_left_y, bottom_right_x, bottom_right_y, other_target_images):
                processed_positions.append(array[0])
                time.sleep(0.1)
                pyautogui.click(*discord_icon)           #discord icon
                time.sleep(0.2)
                pyautogui.click(*discord_loop)              #discord loop search icon
                pyautogui.doubleClick(*discord_loop)
                time.sleep(0.2)
                pyautogui.press('f8')
                time.sleep(0.2)
                pyautogui.press('enter')

                timer = 0
                if timer < 3:
                    time.sleep(1.2)
                    timer += 1

                    # Определяем радиус
                    radius = 5

                    # Координаты центра (белого пикселя)
                    x_center, y_center = white_pixel

                    # Проверяем каждый пиксель в заданном радиусе
                    for x_offset in range(-radius, radius + 1):
                        for y_offset in range(-radius, radius + 1):
                            # Координаты текущего пикселя
                            x = x_center + x_offset
                            y = y_center + y_offset

                            # Получаем цвет текущего пикселя
                            pixel_color = pyautogui.pixel(x, y)

                            # Проверяем, является ли пиксель белым
                            if pixel_color == (255, 255, 255) or pixel_color == (0, 0, 0):
                                # Действия, если обнаружен белый пиксель в радиусе
                                notification.notify(
                                    title='Уведомление',
                                    message=f'Белый пиксель'
                                            f''
                                            f' обнаружен на координатах {x}, {y}. Программа завершает работу.',
                                    timeout=10
                                )
                                exit()
                    '''
                        if pixel_color[0] == 255 and pixel_color[1] == 0 and pixel_color[2] == 0 or pixel_color2[0] == 0 and pixel_color2[1] == 0 and pixel_color2[2] == 0:
    
                        time.sleep(0.2)
    
                        pyautogui.click(*osrs_icon)
    
                        pyautogui.rightClick(bottom_right_x, bottom_right_y)
    
                        continue            
                    '''

                time.sleep(0.2)
                pyautogui.click(*osrs_icon)
                pyautogui.rightClick(bottom_right_x, bottom_right_y)
            else:
                time_elapsed = 0
                while time_elapsed < 4:
                    if find_and_click_second_target(other_target_images, timeout=1):
                        break
                    time.sleep(1)
                    time_elapsed += 1

                click_array(array)  # Кликнуть по следующему красному массиву

        pyautogui.hotkey('F4')
        keyboard.press_and_release('F4')
        print("смена мира")
        arrays = []
        processed_positions = []
        time.sleep(11) """