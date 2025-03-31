from time import time

def progressbar(it, prefix="", bar_size=40, end_print="\n"):
    timeToStr = lambda t: f"{int(t//60):02}:{int(t%60):02}"
    it = it if hasattr(it, '__len__') else list(it)
    count, start = len(it), time()
    if count == 0: return []
    def show(j):
        prec = round(100*j/count)
        bar_length = bar_size  # Hier fehlt die Definition von bar_length
        bar = f"[{'=' * int(prec/100*bar_length)}{' ' * (bar_length - int(prec/100*bar_length))}]"
        t_curr = timeToStr(time()-start)
        t_total = timeToStr(count*(time()-start)/j if j > 0 else 0)
        print(f"{prefix} {prec:>3}%|{bar}| {j:>{len(str(count))}}/{count} [{t_curr}<{t_total}]", end='\r', flush=True)

    show(0.1)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print(end_print, end="", flush=True)
