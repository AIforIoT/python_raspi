import localization as lx

P = lx.Project(mode='2D', solver='LSE')


P.add_anchor('A', (5,0))
P.add_anchor('B', (0,0))
#P.add_anchor('C', (2,2))

t,label=P.add_target()

t.add_measure('A', 0.17*330)
t.add_measure('B', 0.4*330)
#t.add_measure('C', 0.2*330)
print(t.loc.x) 
P.solve()

print(t.loc.y)
print(t.loc.x)
