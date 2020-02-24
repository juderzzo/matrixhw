import math

def print_matrix(matrix):
    x = str()
    y = str()
    z = str()
    one = str()
    for li in matrix:
        x += str(li[0]) + " "
        y += str(li[1]) + " "
        z += str(li[2]) + " "
        one += str(li[3]) + " "
    print(x)
    print(y)
    print(z)
    print(one)

def ident(matrix):
    a = 0
    while a < len(matrix):
        b = 0
        while b < len(matrix):
            if (a == b):
                matrix[a][b] = 1
            else:
                matrix[a][b] = 0
            b += 1
        a += 1

def add_const(matrix, const):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = matrix[i][j] + const


def matrix_mult(m1, m2):
    copy = new_matrix(len(m2[0]), len(m2))
    e = 0
    while e < len(m2):
        a = 0
        while a < len(m1[0]):
            sum = 0
            b = 0
            while b < len(m1):
                sum += m1[b][a] * m2[e][b]
                b += 1
            copy[e][a] = sum
            a += 1
        e += 1
    c = 0
    while c < len(m2):
        d = 0
        while d < len(m2[0]):
            m2[c][d] = copy[c][d]
            d += 1
        c += 1

def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m

def scale_matrix(matrix, const):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j] * const



def draw_lines( matrix, screen, color ):
    for i in range(0,len(matrix),2):
        draw_line(matrix[i][0], matrix[i][1], matrix[i + 1][0], matrix[i + 1][1], screen, color)

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append([x, y, z, 1])



##########################################################################
#show of matricies and shown on website

print("Testing add_edge. Adding (1, 2, 3), (4, 5, 6) m2 =")
m2 = new_matrix(4, 0)
add_edge(m2, 1, 2, 3, 4, 5, 6)
print_matrix(m2)
print("\n")
print("Testing scaling * 2")
scale_matrix(m2, 2)
print_matrix(m2)
print("\n")
print("Testing ident. m1 =")
m1 = new_matrix(4, 4)
ident(m1)
print_matrix(m1)
print("\n")
print("Testing Matrix mult. m1 * m2 =")
matrix_mult(m1, m2)
print_matrix(m2)
print("\n")
print("Testing Matrix mult. m1 =")
del m1[:]
add_edge(m1, 9, 8, 7, 6, 5, 4)
add_point(m1, 3, 2, 1)
add_point(m1, 0, 9, 8)
print_matrix(m1)
print("\n")
print("Testing Matrix mult. m1 * m2 =")
matrix_mult(m1, m2)
print_matrix(m2)
print("\n")



#############################################################
#display functions
from subprocess import Popen, PIPE
from os import remove

#constants
XRES = 500
YRES = 500
MAX_COLOR = 255
RED = 0
GREEN = 1
BLUE = 2

DEFAULT_COLOR = [0, 0, 0]

def new_screen( width = XRES, height = YRES ):
    screen = []
    for y in range( height ):
        row = []
        screen.append( row )
        for x in range( width ):
            screen[y].append( DEFAULT_COLOR[:] )
    return screen

def plot( screen, color, x, y ):
    newy = YRES - 1 - y
    if ( x >= 0 and x < XRES and newy >= 0 and newy < YRES ):
        screen[newy][x] = color[:]

def clear_screen( screen ):
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            screen[y][x] = DEFAULT_COLOR[:]

def save_ppm( screen, fname ):
    f = open( fname, 'wb' )
    ppm = 'P6\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    f.write(ppm.encode())
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            f.write( bytes(pixel) )
    f.close()

def save_ppm_ascii( screen, fname ):
    f = open( fname, 'w' )
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range( len(screen) ):
        row = ''
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            row+= str( pixel[ RED ] ) + ' '
            row+= str( pixel[ GREEN ] ) + ' '
            row+= str( pixel[ BLUE ] ) + ' '
        ppm+= row + '\n'
    f.write( ppm )
    f.close()

def save_extension( screen, fname ):
    ppm_name = fname[:fname.find('.')] + '.ppm'
    save_ppm_ascii( screen, ppm_name )
    p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

def display( screen ):
    ppm_name = 'pic.ppm'
    save_ppm_ascii( screen, ppm_name )
    p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)



###########################

def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line







##############################################################################

screen = new_screen()
color = [ 0, 255, 0 ]
matrix = new_matrix()
add_edge(matrix, -5, -3, 0, -3, -7, 0)
add_edge(matrix, -3, -7, 0, -3, -6, 0)
add_edge(matrix, -3, -6, 0, -2, -4, 0)
add_edge(matrix, -2, -4, 0, -1, 0, 0)
add_edge(matrix, -7, 1, 0, -8, 4, 0)
add_edge(matrix, -2, -4, 0, -1, 0, 0)
add_edge(matrix, -8, 4, 0, -9, 7, 0)
add_edge(matrix, -9, 7, 0, -8, 10, 0)
add_edge(matrix, -8, 10, 0, -7, 10, 0)
add_edge(matrix, -7, 10, 0, -5, 9, 0)
add_edge(matrix, -5, 9, 0, -3, 7, 0)
add_edge(matrix, -3, 7, 0, -2, 6, 0)
add_edge(matrix, -2, 6, 0, 0, 7, 0)
add_edge(matrix, 2, 6, 0, 0, 7, 0)
add_edge(matrix, 2, 6, 0, 3, 7, 0)
add_edge(matrix, 5, 9, 0, 3, 7, 0)
add_edge(matrix, 5, 9, 0, 7, 10, 0)
add_edge(matrix, 8, 10, 0, 7, 10, 0)
add_edge(matrix, 8, 10, 0, 9, 7, 0)
add_edge(matrix, 8, 4, 0, 9, 7, 0)
add_edge(matrix, 8, 10, 0, 7, 1, 0)
add_edge(matrix, 3, 4, 0, 7, 1, 0)
add_edge(matrix, 3, 4, 0, 0, 1, 0)
add_edge(matrix, -3, 4, 0, 0, 1, 0)
add_edge(matrix, -3, 4, 0, -7, 1, 0)
add_edge(matrix, -5, 0, 0, -4, 0, 0)
add_edge(matrix, -2, -1, 0, -4, 0, 0)
add_edge(matrix, -2, -1, 0, -4, -1, 0)
add_edge(matrix, -5, 0, 0, -4, -1, 0)
add_edge(matrix, 5, -3, 0, 4, -5, 0)
add_edge(matrix, 4, -5, 0, 3, -7, 0)
add_edge(matrix, 7, 1, 0, 9, -7, 0)
add_edge(matrix, 8, -7, 0, 9, -7, 0)
add_edge(matrix, 8, -7, 0, 7, -6, 0)
add_edge(matrix, 4, -9, 0, 7, -6, 0)
add_edge(matrix, 4, -9, 0, 1, -10, 0)
add_edge(matrix, -1, -10, 0, 1, -10, 0)
add_edge(matrix, -1, -10, 0, -4, -9, 0)
add_edge(matrix, -7, -6, 0, -4, -9, 0)
add_edge(matrix, -7, -6, 0, -8, -7, 0)
add_edge(matrix, -9, -6, 0, -8, -7, 0)
add_edge(matrix, -9, -6, 0, -8, -2, 0)
add_edge(matrix, -7, -1, 0, -8, -2, 0)
add_edge(matrix, 5, 0, 0, 4, -1, 0)
add_edge(matrix, -2, -1, 0, 4, -1, 0)
add_edge(matrix, -2, -1, 0, 4, 0, 0)
add_edge(matrix, 5, 0, 0, 4, 0, 0)
add_edge(matrix, 1, 0, 0, 2, -4, 0)
add_edge(matrix, 3, -6, 0, 2, -4, 0)
add_edge(matrix, 3, -6, 0, 3, -7, 0)
add_edge(matrix, 1, -8, 0, 3, -7, 0)
add_edge(matrix, -4, -1, 0, -4, 0, 0)
add_edge(matrix, -3, -1, 0, -4, 0, 0)
add_edge(matrix, -3, -7, 0, -1, -8, 0)
add_edge(matrix, 1, -8, 0, -1, -8, 0)
add_edge(matrix, 1, -8, 0, 2, -6, 0)
add_edge(matrix, 1, -5, 0, 2, -6, 0)
add_edge(matrix, 1, -5, 0, -1, -5, 0)
add_edge(matrix, -2, -6, 0, -1, -5, 0)
add_edge(matrix, -2, -6, 0, -1, -8, 0)
add_edge(matrix, 4, 6, 0, 7, 9, 0)
add_edge(matrix, 7, 9, 0, 7, 5, 0)
add_edge(matrix, 6, 4, 0, 7, 5, 0)
add_edge(matrix, 6, 4, 0, 4, 5, 0)
add_edge(matrix, 4, 6, 0, 4, 5, 0)
add_edge(matrix, 4, -1, 0, 4, 0, 0)
add_edge(matrix, 3, -1, 0, 4, 0, 0)
add_edge(matrix, -7, 4, 0, -7, 9, 0)
add_edge(matrix, -4, 6, 0, -7, 9, 0)
add_edge(matrix, -4, 6, 0, -4, 5, 0)
add_edge(matrix, -6, 3, 0, -4, 5, 0)
add_edge(matrix, -6, 3, 0, -7, 4, 0)

scale_matrix(matrix, 30)
add_const(matrix, 250)


#print(screen)

draw_lines( matrix, screen, color )
#print(screen)
file = open("image.ppm", "w")
file.write("P3\n500 500\n255\n")
for i in screen:
    for j in i:

        file.write(str(j[0]) + ' ' + str(j[1]) + ' ' + str(j[2]))
        file.write("\n")
file.close()
