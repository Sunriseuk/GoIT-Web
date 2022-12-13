from time import time
from multiprocessing import Process, Pool, cpu_count

def factorize(*numbers):
    for number in numbers:
        div = []
        for divisors in range (1, number+1):
            if number % divisors == 0:
                div.append(divisors)
        print(f'Divisors of {number} is {div}')
        




if __name__ == '__main__':
    processors = cpu_count()
    t1 = time()
    result = factorize(128, 255, 99999, 10651060, 106510609)
    print()
    print(f'час виконання лінійно: {time() - t1}')
    print()
    t2 = time()
    pool = Pool(processors)
    result = pool.apply_async(factorize, (128, 255, 99999, 10651060, 106510609))
    print(f'час виконання на {processors} процесорах {time() - t2}')
    print(result.get())