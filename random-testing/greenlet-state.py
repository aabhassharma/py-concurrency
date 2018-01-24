import gevent


def win():
    return 'You win!'


def fail():
    raise Exception('You fail at failing!')


winner = gevent.spawn(win)
loser = gevent.spawn(fail)

print(winner.started)
print(loser.started)

try:
    gevent.joinall([winner, loser])
except Exception as e:
    print('This will never be reached')

print(winner.value)
print(loser.value)

print(winner.ready())
print(loser.ready())

# Doesn't seem to work 
# print(winner.succesful())
# print(loser.successful())

print(loser.exception)
