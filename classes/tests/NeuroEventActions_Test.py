from . import NeuroEventActions as NEA

scores = [
    ('Выбрала вилку', 33),
    ('Бандерокошкодівка', 27),
    ('Дев?чка в?лшебница Усаги-чан', 25)
]

print(NEA.Finishing()._make_top(scores))