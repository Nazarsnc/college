sn = "Синиця"
n = "Назар"
a = 16
fn = sn + " " + n
list = [fn]

if type(sn) == type(n):
    print(f"type: {type(sn)}")
    print(list[0])
    if type(a) == int:
        print(type(a))
        print(a)
    else:
        print("Помилка")
else:
    print("Помилка")