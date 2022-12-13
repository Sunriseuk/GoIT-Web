from time import time
from multiprocessing import Process

def factorize(*numbers):
    for number in numbers:
        div = []
        for divisors in range (1, number+1):
            if number % divisors == 0:
                div.append(divisors)
        print(f'Divisors of {number} is {div}')
        







if __name__ == '__main__':
    before = time()
    print('hello')
    for i in range(4):
        pr = Process(target=factorize)
        pr.start()
    
factorize(128, 255, 99999, 10651060)

after = time()
print()
print(f'Work-time is {after-before} seconds')



# def download_all(count: int):
#     pool = Pool(4)
#     pool.map(download, range(count))


# download_all(15)