#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 32000000), ('example2.txt', 11687500), ('input.txt', 866435264)])

linecount = len(list(case_lines()))

queue = deque() # of tuples (source_name, dest_name, pulse_value)

modules = defaultdict(lambda: Sink(name="<anonymous>", destinations=[]))

class Module:
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.sources = None

    def set_sources(self, sources):
        self.sources = sources

    def receive(self, source, pulse_value): # pulse value low == False, high == True
        raise NotImplementedError

    def send(self, pulse_value):
        for destination in self.destinations:
            # print(f'{self.name} -{"high" if pulse_value else "low"}-> {destination}')
            queue.append((self.name, destination, pulse_value))

class FlipFlop(Module):
    def __init__(self, **args):
        super().__init__(**args)
        self.state = False

    def receive(self, source, pulse_value):
        if not pulse_value:
            self.state = not self.state
            self.send(self.state)

class Conjunction(Module):
    def __init__(self, **args):
        super().__init__(**args)
        self.state = {}

    def receive(self, source, pulse_value):
        self.state[source] = pulse_value
        self.send(not all(self.state.values()))

    def set_sources(self, sources):
        self.sources = sources
        self.state = {s:False for s in sources}

class Broadcaster(Module):
    def receive(self, source, pulse_value):
        self.send(pulse_value)

class Button(Module):
    def click(self):
        self.send(False)

class Sink(Module):
    def receive(self, source, pulse_value):
        pass

def load():
    for line in case_lines():
        parts = line.split('->')
        name = parts[0].strip()
        destinations = [p.strip() for p in parts[1].split(',')]
        match name[0]:
            case '%':
                modules[name[1:]] = FlipFlop(name=name[1:], destinations=destinations)
            case '&':
                modules[name[1:]] = Conjunction(name=name[1:], destinations=destinations)
            case 'b':
                modules[name] = Broadcaster(name=name, destinations=destinations)
            case _:
                raise NotImplementedError
    
    d2s = defaultdict(lambda: [])
    for m in modules.values():
        for d in m.destinations:
            d2s[d].append(m.name)
    for destination,sources in d2s.items():
        modules[destination].set_sources(sources)

def run(n_times):
    load()
    button = Button(name="button", destinations=["broadcaster"])

    counts = {True: 0, False: 0}
    for _ in range(n_times):
        button.click()

        while queue:
            source, destination, pulse_value = queue.popleft()
            counts[pulse_value] += 1
            print(f'{source} -{"high" if pulse_value else "low"}-> {destination}')
            modules[destination].receive(source, pulse_value)
    
    return counts[True],counts[False]

assert_solution(prod(run(1000)))