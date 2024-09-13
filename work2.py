sn = "Синиця"
n = "Назар"
a = 16
fn = f"{sn} {n}"
list = [fn,a]

if type(sn) == type(n):
    print(f"type: {type(sn)}")
    print(f"FullName: {list[0]}")
    if type(a) == int:
        print(f"type: {type(a)}")
        print(f"Age: {list[1]}")
    else:
        print("Помилка")
else:
    print("Помилка")
