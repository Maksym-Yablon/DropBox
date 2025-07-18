# 🎨 Технічне завдання для художника

## Котики-фігури для гри DropBox

### 📐 Технічні вимоги:
- **Розмір**: 32x32 пікселів на один блок
- **Формат**: PNG з прозорістю
- **Стиль**: Мілий пікселарт або векторна графіка
- **Кольори**: Яскраві, веселі кольори

### 🐱 Фігури котиків:

#### 1. **I_piece** (Паличка) - Довгий котик
- **Поза**: Розтягнувся в лінію (4 блоки)
- **Ідея**: Котик сплить або потягується
- **Розмір**: 128x32 пікселів або 32x128 (залежно від орієнтації)

#### 2. **O_piece** (Квадрат) - Кругленький котик  
- **Поза**: Згорнувся клубочком
- **Ідея**: Сплячий котик калачиком
- **Розмір**: 64x64 пікселів

#### 3. **T_piece** (Трійка) - Котик з хвостом
- **Поза**: Сидить, хвіст в сторону
- **Ідея**: Котик дивиться вперед, хвіст в бік
- **Розмір**: 96x64 пікселів

#### 4. **S_piece** (Зміка) - Грайливий котик
- **Поза**: Вигнувся дугою
- **Ідея**: Котик грається або потягується
- **Розмір**: 96x64 пікселів

#### 5. **Z_piece** (Зворотна зміка) - Котик навпаки
- **Поза**: Вигнувся у протилежний бік
- **Ідея**: Дзеркальна версія S_piece
- **Розмір**: 96x64 пікселів

#### 6. **J_piece** (Гачок) - Котик дивиться вгору
- **Поза**: Сидить, дивиться вгору
- **Ідея**: Котик піднявся на задні лапи
- **Розмір**: 64x96 пікселів

#### 7. **L_piece** (Зворотний гачок) - Котик дивиться в інший бік
- **Поза**: Дзеркальна версія J_piece
- **Ідея**: Котик дивиться в протилежний бік
- **Розмір**: 64x96 пікселів

### 🎭 Анімаційні стани для кожного котика:

1. **idle.png** - Спокійний стан (базова поза)
2. **falling.png** - Падає (можливо, трохи розмитий)
3. **rotating.png** - Крутиться (ефект обертання)
4. **landing.png** - Приземляється (трохи сплющений)
5. **happy.png** - Радіє (коли лінія очищається)

### 🎨 Рекомендації по стилю:

- **Вирази мордочок**: Мілі, дружні
- **Кольори**: Різні породи котів (рудий, сірий, чорний, білий)
- **Деталі**: Великі очі, маленькі носики
- **Консистентність**: Всі котики в одному стилі

### 📁 Структура файлів:

```
assets/sprites/cats/
├── I_piece/
│   ├── idle.png
│   ├── falling.png
│   ├── rotating.png
│   ├── landing.png
│   └── happy.png
├── O_piece/
│   └── (те саме)
└── ... (для всіх фігур)
```

### 🔊 Звукові ефекти (бонус):

- **meow_land.wav** - М'яке мяукання при приземленні
- **purr_rotate.wav** - Муркотіння при обертанні
- **happy_clear.wav** - Радісне мяукання при очистці лінії
- **sad_gameover.wav** - Сумне мяукання при програші

### 💡 Додаткові ідеї:

- Котики різних порід для різних фігур
- Сезонні костюми (шапочки, бантики)
- Різні емоції залежно від швидкості гри
- Спеціальні ефекти при комбо
