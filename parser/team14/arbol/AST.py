reservadas = {
    'show': 'show',
    'database': 'databases',
    'like': 'like',
    'select': 'select',
    'distinct': 'distinct',
    'from': 'r_from',
    'alter': 'alter',
    'rename': 'rename',
    'to': 'to',
    'owner': 'owner',
    'table': 'table',
    'add': 'add',
    'column': 'column',
    'set': 'set',
    'not': 'not',
    'null': 'null',
    'check': 'check',
    'constraint': 'constraint',
    'unique': 'unique',
    'foreign': 'foreign',
    'key': 'key',
    'or': 'or',
    'replace': 'replace',
    'if': 'if',
    'exists': 'exist',
    'mode': 'mode',
    'inherits': 'inherits',
    'primary': 'primary',
    'references': 'references',
    'default': 'default',
    'type': 'type',
    'enum': 'enum',
    'drop': 'drop',
    'update': 'update',
    'where': 'where',
    'smallint': 'smallint',
    'integer': 'integer',
    'bigint': 'bigint',
    'decimal': 'decimal',
    'numeric': 'numeric',
    'real': 'real',
    'double': 'double',
    'precision': 'precision',
    'money': 'money',
    'character': 'character',
    'varying': 'varying',
    'char': 'char',
    'timestamp': 'timestamp',
    'without': 'without',
    'zone': 'zone',
    'date': 'date',
    'time': 'time',
    'interval': 'interval',
    'boolean': 'boolean',
    'true': 'true',
    'false': 'false',
    'year': 'year',
    'month': 'month',
    'day': 'day',
    'hour': 'hour',
    'minute': 'minute',
    'second': 'second',
    'in': 'in',
    'and': 'and',
    'between': 'between',
    'symetric': 'symetric',
    'isnull': 'isnull',
    'notnull': 'notnull',
    'unknown': 'unknown',
    'insert': 'insert',
    'into': 'into',
    'values': 'values',
    'group': 'group',
    'by': 'by',
    'having': 'having',
    'as': 'as',
    'create': 'create',
    'varchar': 'varchar',
    'text': 'text',
    'is': 'is',
    'delete': 'delete',
    'order': 'order',
    'asc' : 'asc',
    'desc' : 'desc',
    'when': 'when',
    'case': 'case',
    'else': 'else',
    'then': 'then',
    'end': 'end',
    'extract':'extract',
    'current_time':'current_time',
    'current_date':'current_date',
    'any':'any',
    'all':'all',
    'some':'some',
    'limit': 'limit',
    'offset': 'offset',
    'union': 'union',
    'except': 'except',
    'intersect': 'intersect',
    'with':'with'

}

tokens = [
             'mas',
             'menos',
             'elevado',
             'multiplicacion',
             'division',
             'modulo',
             'menor',
             'mayor',
             'igual',
             'menor_igual',
             'mayor_igual',
             'diferente1',
             'diferente2',
             'ptcoma',
             'para',
             'coma',
             'punto',
             'int',
             'decimales',
             'cadena',
             'cadenaString',
             'parc',
             'id'
         ] + list(reservadas.values())

# Tokens
t_mas = r'\+'
t_menos = r'-'
t_elevado = r'\^'
t_multiplicacion = r'\*'
t_division = r'/'
t_modulo = r'%'
t_menor = r'<'
t_mayor = r'>'
t_igual = r'='
t_menor_igual = r'<='
t_mayor_igual = r'>='
t_diferente1 = r'<>'
t_diferente2 = r'!='
t_para = r'\('
t_parc = r'\)'
t_ptcoma = r';'
t_coma = r','
t_punto = r'\.'

def t_decimales(t):
    r'\d+\.\d+([e][+-]\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error no se puede convertir %d", t.value)
        t.value = 0
    return t

def t_int(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Valor numerico incorrecto %d", t.value)
        t.value = 0
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value.lower(), 'id')
    return t

def t_cadena(t):
    r'\'.*?\''
    t.value = t.value[1:-1]  # remuevo las comillas
    return t

def t_cadenaString(t):
    r'".*?"'
    t.value = t.value[1:-1]  # remuevo las comillas
    return t


# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*/*([^\*/]|[^\*]/|\*[^/])*\**\*/'
    t.lexer.lineno += t.value.count('\n')


# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'--.*\n'
    t.lexer.lineno += 1


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construyendo el analizador léxico
import ply.lex as lex

lexer = lex.lex()

from graphviz import Digraph
arbol = Digraph(comment='Árbol Sintáctico Abstracto (AST)', 
node_attr={'fillcolor':'darkolivegreen','color':'darkolivegreen','style':'filled','fontcolor':'white'},
edge_attr={'arrowsize':'0.7'},graph_attr={'label':'Árbol Sintáctico Abstracto (AST)'})
arbol.node_attr.update(color = 'navyblue')

i = 0
def inc():
    global i
    i += 1
    s = str(i)
    return s

# Asociación de operadores y precedencia
precedence = (
    ('left', 'or'),
    ('left', 'and'),
    ('right', 'not'),
    ('left', 'predicates'),
    ('left', 'mayor', 'menor', 'mayor_igual', 'menor_igual', 'igual', 'diferente1', 'diferente2'),
    ('left', 'mas', 'menos'),
    ('left', 'multiplicacion', 'division', 'modulo'),
    ('left', 'elevado'),
    ('right', 'umenos', 'umas'),
    ('left', 'punto'),
    ('left', 'lsel'),
)


# ----------------------------------------------DEFINIMOS LA GRAMATICA------------------------------------------
# Definición de la gramática


def p_init(t):
    'init            : instrucciones'
    id = inc()
    t[0] = id
    arbol.node(id,"INIT")
    arbol.edge(id,t[1])
    print("ok")


def p_instrucciones_lista(t):
    'instrucciones    : instrucciones instruccion'
    t[0] = t[1]
    arbol.edge(t[1],t[2])


def p_instrucciones_instruccion(t):
    'instrucciones    : instruccion '
    id = inc()
    t[0] = id
    arbol.node(id,"INSTRUCCION")
    arbol.edge(id,t[1])


def p_instruccion(t):
    '''instruccion      :  SELECT ptcoma
                    | CREATETABLE
                    | UPDATE ptcoma
                    | DELETE  ptcoma
                    | ALTER  ptcoma
                    | DROP ptcoma
                    | INSERT ptcoma
                    | CREATETYPE ptcoma
                    | CASE 
                    | CREATEDB ptcoma
                    | SHOWDB ptcoma'''
    t[0] = t[1]


def p_CASE(t):
    ''' CASE : case  LISTAWHEN ELSE end
               | case LISTAWHEN end'''
    id = inc()
    t[0] = id
    arbol.node(id,"CASE")
    arbol.edge(id,t[2])
    if len(t) > 4: arbol.edge(id,t[3])

def p_LISTAWHEN(t):
    ''' LISTAWHEN : LISTAWHEN WHEN'''
    t[0] = t[1]
    arbol.edge(t[1],t[2])

def p_LISTAWHEN1(t):
    ''' LISTAWHEN : WHEN'''
    id = inc()
    t[0] = id
    arbol.node(id,"WHEN")
    arbol.edge(id,t[1])

def p_WHEN(t): 
    ''' WHEN : when LEXP then LEXP'''
    id = inc()
    t[0] = id
    arbol.node(id,"when")
    lxpA = t[2]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))
    th = inc()
    arbol.node(th,"then")
    arbol.edge(id,th)
    lxpA = t[4]
    for x in range(len(lxpA)):
        arbol.edge(th,str(lxpA[x]))

def p_ELSE(t):
    '''ELSE : else LEXP'''
    id = inc()
    t[0] = id
    arbol.node(id,"else")
    lxpA = t[2]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

def p_INSERT(t):
    '''INSERT : insert into id values para LEXP parc'''
    id = inc()
    t[0] = id
    arbol.node(id,"insert")
    into = inc()
    arbol.node(into,"into")
    arbol.edge(id,into)
    iden = inc()
    arbol.node(iden,str(t[3]))
    arbol.edge(into,iden)
    val = inc()
    arbol.node(val,"values")
    arbol.edge(id,val)
    lxpA = t[6]
    for x in range(len(lxpA)):
        arbol.edge(val,str(lxpA[x]))

def p_DROP(t):
    '''DROP : drop table id
             | drop databases id '''
    id = inc()
    t[0] = id
    arbol.node(id,"drop")
    at = inc()
    arbol.node(at,str(t[2]))
    arbol.edge(id,at)
    ide = inc()
    arbol.node(ide,str(t[3]))
    arbol.edge(at,ide)

def p_DROP1(t):
    '''DROP : drop databases if exist id'''
    id = inc()
    t[0] = id
    arbol.node(id,"drop")
    at = inc()
    arbol.node(at,"databases if exist")
    arbol.edge(id,at)
    ide = inc()
    arbol.node(ide,str(t[5]))
    arbol.edge(at,ide)

def p_ALTER(t):
    '''ALTER : alter databases id RO
            | alter table id OP'''
    id = inc()
    t[0] = id
    arbol.node(id,"alter")
    at = inc()
    arbol.node(at,str(t[2]))
    arbol.edge(id,at)
    ide = inc()
    arbol.node(ide,str(t[3]))
    arbol.edge(at,ide)
    arbol.edge(id,t[4])

def p_r_o(t):
    '''RO : rename to id
           | owner to id'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))
    iden = inc()
    arbol.node(iden,str(t[3]))
    arbol.edge(id,iden)

def p_op(t):
    '''OP : add ADD '''
    id = inc()
    t[0] = id
    arbol.node(id,"add")
    arbol.edge(id,t[2])

def p_op1(t):
    '''OP :  drop column ALTERDROP
            | drop ALTERDROP'''
    id = inc()
    t[0] = id
    arbol.node(id,"drop")
    if len(t) > 3: arbol.edge(id,t[3])
    else : arbol.edge(id,t[2])

def p_op2(t):
    '''OP : alter column id set not null
            | alter column id set null'''
    id = inc()
    t[0] = id
    arbol.node(id,"alter")
    cc = inc()
    arbol.node(cc,"column")
    arbol.edge(id,cc)
    ic = inc()
    arbol.node(ic,str(t[3]))
    arbol.edge(cc,ic)
    ss = inc()
    arbol.node(ss,"set")
    arbol.edge(id,ss)
    ccc = str(t[5])
    if len(t) > 5: ccc += " " + str(t[6])
    nn = inc()
    arbol.node(nn,ccc)
    arbol.edge(ss,nn)

def p_op3(t):
    '''OP : rename column id to id'''
    id = inc()
    t[0] = id
    arbol.node(id,"rename")
    cc = inc()
    arbol.node(cc,"column")
    arbol.edge(id,cc)
    ic = inc()
    arbol.node(ic,str(t[3]))
    arbol.edge(cc,ic)
    tc = inc()
    arbol.node(tc,"to")
    arbol.edge(id,tc)
    itc = inc()
    arbol.node(tc,str(t[5]))
    arbol.edge(itc,tc)

def p_op4(t):
    '''OP : listaalc'''
    t[0] = t[1]

def p_listaalc1(t):
    '''listaalc : listaalc coma alc'''
    t[0] = t[1]
    arbol.edge(t[1],t[3])

def p_listaalc2(t):
    '''listaalc : alc'''
    id = inc()
    t[0] = id
    arbol.node(id,"alter")
    arbol.edge(id,t[1])

def p_alc(t):
    '''alc : alter column id type TIPO'''
    id = inc()
    t[0] = id
    arbol.node(id,"column")
    iden = inc()
    arbol.node(iden,t[3])
    arbol.edge(id,iden)
    arbol.edge(iden,t[5])

def p_ALTERDROP(t):
    '''ALTERDROP : constraint id
                | check id'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))
    iden = inc()
    arbol.node(id,str(t[2]))
    arbol.edge(id,iden)

def p_ALTERDROP1(t):
    '''ALTERDROP : column LEXP'''
    id = inc()
    t[0] = id
    arbol.node(id,"column")
    lxpA = t[2]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))
    
def p_ADD1(t):
    '''ADD : column id TIPO'''
    id = inc()
    t[0] = id
    arbol.node(id,"column")
    iden = inc()
    arbol.node(iden,str(t[2]))
    arbol.edge(id,iden)
    arbol.edge(id,t[3])

def p_ADD2(t):
    '''ADD : check para LEXP parc'''
    id = inc()
    t[0] = id
    arbol.node(id,"check")
    lxpA = t[3]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

def p_ADD3(t):
    '''ADD : constraint id unique para id parc'''
    id = inc()
    t[0] = id
    arbol.node(id,"constraint")
    iden = inc()
    arbol.node(iden,str(t[2]))
    arbol.edge(id,iden)
    uu = inc()
    arbol.node(uu,"unique")
    arbol.edge(id,uu)
    iu = inc()
    arbol.node(iu,str(t[5]))
    arbol.edge(uu,iu)

def p_ADD4(t):
    '''ADD : foreign key para LEXP parc references id para LEXP parc'''
    id = inc()
    t[0] = id
    arbol.node(id,"foreign key")
    lxpA = t[4]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

    rr = inc()
    arbol.node(rr,"references")
    arbol.edge(id,rr)
    ir = inc()
    arbol.node(ir,str(t[7]))
    arbol.edge(rr,ir)
    lxpA = t[9]
    for x in range(len(lxpA)):
        arbol.edge(rr,str(lxpA[x]))

def p_SHOWDB(t) : 
   ''' SHOWDB : show databases'''
   id = inc()
   t[0] = id
   arbol.node(id, "show databases")

def p_CREATEDB1(t) : 
    '''CREATEDB : create RD if not exist id
                | create RD if not exist id OPCCDB'''
    id = inc()
    t[0] = id
    arbol.node(id,("create " + t[2] + " if not exist"))
    iden = inc()
    arbol.node(iden,str(t[6]))
    arbol.edge(id,iden)
    if len(t) > 7:
        arr = t[7]
        arbol.edge(id,arr[0])
        if len(arr) > 1:
            arbol.edge(id,arr[1])

def p_CREATEDB2(t) : 
    '''CREATEDB : create RD id
                | create RD id OPCCDB'''
    id = inc()
    t[0] = id
    arbol.node(id,("create " + t[2]))
    iden = inc()
    arbol.node(iden,str(t[3]))
    arbol.edge(id,iden)
    if len(t) > 4:
        arr = t[4]
        arbol.edge(id,arr[0])
        if len(arr) > 1:
            arbol.edge(id,arr[1])

def p_OPCCDB(t):
    '''OPCCDB : PROPIETARIO
        | MODO
        | PROPIETARIO MODO'''
    if len(t) > 2: t[0] = [t[1],t[2]]
    else: t[0] = [t[1]]

def p_RD(t) : 
    '''RD : or replace databases
        | databases'''
    c = str(t[1])
    if len(t) > 2: c += str(" " + t[2] + " " + t[3])

    t[0] = c
 
def p_PROPIETARIO(t):
    '''PROPIETARIO : owner igual id
		| owner id'''
    id = inc()
    t[0] = id
    arbol.node(id,"owner")
    tt = inc()
    if len(t) == 3: arbol.node(tt,str(t[2]))
    else: arbol.node(tt,str(t[3]))
    arbol.edge(id,tt)

def p_MODO(t): 
    '''MODO : mode  igual int
	    | mode int
    '''	
    id = inc()
    t[0] = id
    arbol.node(id,"mode")
    tt = inc()
    if len(t) == 3: arbol.node(tt,str(t[2]))
    else: arbol.node(tt,str(t[3]))
    arbol.edge(id,tt)


def p_CREATETABLE(t):
    '''CREATETABLE : create table id para LDEF parc ptcoma
                    | create table id para LDEF parc HERENCIA ptcoma'''
    id = inc()
    t[0] = id
    arbol.node(id,"create table")
    iden = inc()
    arbol.node(iden,str(t[3]))
    arbol.edge(id,iden)
    arbol.edge(id,t[5])
    if len(t) > 8:
        arbol.edge(id,t[7])

def p_LDEF1(t):
    '''LDEF : LDEF coma COLDEF'''
    t[0] = t[1]
    arbol.edge(t[1],t[3])

def p_LDEF2(t):
    '''LDEF : COLDEF'''
    id = inc()
    t[0] = id
    arbol.node(id,"CONTENIDO")
    arbol.edge(id,t[1])

def p_COLDEF(t):
    '''COLDEF : OPCONST'''
    t[0] = t[1]

def p_COLDEF1(t):
    '''COLDEF : constraint id OPCONST'''
    id = inc()
    t[0] = id
    arbol.node(id,"constraint")
    iden = inc()
    arbol.node(iden,str(t[2]))
    arbol.edge(id,iden)
    arbol.edge(id,t[3])

def p_COLDEF2(t):
    '''COLDEF : id TIPO
                | id TIPO LOPCOLUMN'''
    id = inc()
    t[0] = id
    arbol.node(id,"columna")
    iden = inc()
    arbol.node(iden,str(t[1]))
    arbol.edge(id,iden)
    arbol.edge(id,t[2])
    if len(t) > 3:
        arbol.edge(id,t[3])

def p_LOPCOLUMN1(t):
    '''LOPCOLUMN : LOPCOLUMN OPCOLUMN'''
    t[0] = t[1]
    arbol.edge(t[1],t[2])

def p_LOPCOLUMN2(t):
    '''LOPCOLUMN : OPCOLUMN'''
    id = inc()
    t[0] = id
    arbol.node(id,"ATRCOLUMNA")
    arbol.edge(id,t[1])

def p_OPCOLUMN11(t):
    '''OPCOLUMN : constraint id unique'''
    id = inc()
    t[0] = id
    arbol.node(id,"constraint")
    uu = inc()
    arbol.node(uu,"unique")
    arbol.edge(id,uu)
    iden = inc()
    arbol.node(iden,str(t[2]))
    arbol.edge(uu,iden)

def p_OPCOLUMN12(t):
    '''OPCOLUMN : not null
                | primary key
                | null'''
    id = inc()
    t[0] = id
    if len(t) == 2:
        arbol.node(id,str(t[1]))
    else: 
        arbol.node(id,str(t[1] + " " + t[2]))

def p_OPCOLUMN13(t):
    '''OPCOLUMN : references id'''
    id = inc()
    t[0] = id
    arbol.node(id,"references")
    iden = inc()
    arbol.node(iden,str(t[2]))
    arbol.edge(id,iden)

def p_OPCOLUMN2(t):
    '''OPCOLUMN : constraint id check para EXP parc'''
    id = inc()
    t[0] = id
    arbol.node(id,"constraint")
    iden = inc()
    arbol.node(iden,str(t[2]))
    arbol.edge(id,iden)
    cc = inc()
    arbol.node(cc,"check")
    arbol.edge(id,cc)
    arbol.edge(cc,t[5])

def p_OPCOLUMN3(t):
    '''OPCOLUMN : default EXP'''
    id = inc()
    t[0] = id
    arbol.node(id,"default")
    arbol.edge(id,t[2])

def p_OPCONST1(t):
    '''OPCONST : primary key para LEXP parc
            | foreign key para LEXP parc references id para LEXP parc'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1] + " " + t[2]))
    lxpA = t[4]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

    if len(t) > 6:
        rr = inc()
        arbol.node(rr,"references")
        arbol.edge(id,rr)
        iden = inc()
        arbol.node(iden,str(t[7]))
        arbol.edge(rr,iden)
        lxpA = t[9]
        for x in range(len(lxpA)):
            arbol.edge(rr,str(lxpA[x]))
    

def p_OPCONST2(t):
    '''OPCONST : unique para LEXP parc
                | check para LEXP parc'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))
    lxpA = t[3]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

def p_HERENCIA(t):
    'HERENCIA : inherits para LEXP parc'
    id = inc()
    t[0] = id
    arbol.node(id,"inherits")
    lxpA = t[3]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

def p_CREATETYPE(t):
    'CREATETYPE : create type id as enum para LEXP parc'
    id = inc()
    t[0] = id
    arbol.node(id,"create type")
    iden = inc()
    arbol.node(iden,str(t[3]))
    arbol.edge(id,iden)
    ee = inc()
    arbol.node(ee,"enum")
    arbol.edge(id,ee)
    lxpA = t[7]
    for x in range(len(lxpA)):
        arbol.edge(ee,str(lxpA[x]))

def p_SELECT1(t):
    ''' SELECT : select distinct  LEXP r_from LEXP  WHERE GROUP HAVING COMBINING ORDER LIMIT''' 
    id = inc()
    t[0] = id
    arbol.node(id,"select")
    lxpA = t[3]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

    f = inc()
    arbol.node(f,"from")
    arbol.edge(id,f)
    lxpA = t[5]
    for x in range(len(lxpA)):
        arbol.edge(f,str(lxpA[x]))

    if t[6] != None:
        arbol.edge(id,t[6])
    if t[7] != None:
        arbol.edge(id,t[7])
    if t[8] != None:
        arbol.edge(id,t[8])
    if t[9] != None:
        arbol.edge(id,t[9])
    if t[10] != None:
        arbol.edge(id,t[10])
    if t[11] != None:
        arbol.edge(id,t[11]) 

def p_SELECT2(t):
    ''' SELECT : select  LEXP r_from LEXP WHERE  GROUP HAVING  COMBINING ORDER LIMIT''' 
    id = inc()
    t[0] = id
    arbol.node(id,"select")
    lxpA = t[2]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

    f = inc()
    arbol.node(f,"from")
    arbol.edge(id,f)
    lxpA = t[4]
    for x in range(len(lxpA)):
        arbol.edge(f,str(lxpA[x]))

    if t[5] != None:
        arbol.edge(id,t[5])
    if t[6] != None:
        arbol.edge(id,t[6])
    if t[7] != None:
        arbol.edge(id,t[7])
    if t[8] != None:
        arbol.edge(id,t[8])
    if t[9] != None:
        arbol.edge(id,t[9])
    if t[10] != None:
        arbol.edge(id,t[10])

def p_SELECT3(t):
    ''' SELECT : select  LEXP WHERE  GROUP HAVING  COMBINING ORDER LIMIT''' 
    id = inc()
    t[0] = id
    arbol.node(id,"select")
    lxpA = t[2]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))
        
    if t[3] != None:
        arbol.edge(id,t[3])
    if t[4] != None:
        arbol.edge(id,t[4])
    if t[5] != None:
        arbol.edge(id,t[5])
    if t[6] != None:
        arbol.edge(id,t[6])
    if t[7] != None:
        arbol.edge(id,t[7])
    if t[8] != None:
        arbol.edge(id,t[8])

def p_LIMIT(t):
    '''LIMIT : limit int
               | limit all
               | offset int
               | limit int offset int
               | offset int limit int
               | limit all offset int
               | offset int limit all
               | '''
    tam = len(t)
    if tam > 1:
        id = inc()
        t[0] = id
        if tam == 3:
            arbol.node(id,(str(t[1]) + " " + str(t[2])))
        elif tam == 5:
            arbol.node(id,(str(t[1]) + " " + str(t[2]) + " " + str(t[3]) + " " + str(t[4])))
    else: t[0] = None

def p_WHERE(t):
    ''' WHERE : where LEXP
                | union LEXP
                | union all LEXP
	            | '''
    tam = len(t)
    if tam > 1:
        id = inc()
        t[0] = id
        if tam == 3:
            arbol.node(id,str(t[1]))
            lxpA = t[2]
            for x in range(len(lxpA)):
                arbol.edge(id,str(lxpA[x]))

        elif tam == 4:
            arbol.node(id,str(t[1] + " " + t[2]))
            lxpA = t[3]
            for x in range(len(lxpA)):
                arbol.edge(id,str(lxpA[x]))

    else: t[0] = None

def p_WHERE1(t):
    ''' WHERE : where EXIST'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))
    arbol.edge(id,t[2])

def p_COMBINING(t):
    '''COMBINING :  union LEXP
                | union all LEXP
                | intersect LEXP
                | intersect all LEXP
                | except LEXP
                | except all LEXP
	            | '''
    if len(t) > 1:
        id = inc()
        t[0] = id
        if len(t) == 3:
            arbol.node(id,str(t[1]))
            lxpA = t[2]
            for x in range(len(lxpA)):
                arbol.edge(id,str(lxpA[x]))
        elif len(t) == 4:
            arbol.node(id,str(t[1] + " " + t[2]))
            lxpA = t[3]
            for x in range(len(lxpA)):
                arbol.edge(id,str(lxpA[x]))
    else: t[0] = None


def p_GROUP(t):
    ''' GROUP :  group by LEXP
	            | '''
    if len(t) > 1:
        id = inc()
        t[0] = id
        arbol.node(id,"group by")
        lxpA = t[3]
        for x in range(len(lxpA)):
            arbol.edge(id,str(lxpA[x]))
    else: t[0] = None


def p_HAVING(t):
    ''' HAVING : having LEXP
	| '''
    if len(t) > 1:
        id = inc()
        t[0] = id
        arbol.node(id,"having")
        lxpA = t[2]
        for x in range(len(lxpA)):
            arbol.edge(id,str(lxpA[x]))
    else: t[0] = None

def p_ORDER(t):
    ''' ORDER : order by LEXP ORD
            | order by LEXP
            |  '''
    if len(t) > 1:
        id = inc()
        t[0] = id
        arbol.node(id,"order by")
        lxpA = t[3]
        for x in range(len(lxpA)):
            arbol.edge(id,str(lxpA[x]))
        if len(t) == 5:
            arbol.edge(id,t[4])
    else: t[0] = None

def p_ORD(t):
    ''' ORD : asc
	| desc '''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))

def p_UPDATE(t):
    ' UPDATE : update id set LCAMPOS where LEXP'
    id = inc()
    t[0] = id
    arbol.node(id,"update")
    idd = inc()
    arbol.node(idd,str(t[2]))
    arbol.edge(id,idd)
    arbol.edge(id,t[4])
    ww = inc()
    arbol.node(ww,"where")
    arbol.edge(id,ww)
    lxpA = t[6]
    for x in range(len(lxpA)):
        arbol.edge(ww,str(lxpA[x]))


def p_LCAMPOS1(t):
    '''LCAMPOS :  LCAMPOS id igual EXP'''
    t[0] = t[1]
    ii = inc()
    arbol.node(ii,"=")
    arbol.edge(t[1],ii)
    idd = inc()
    arbol.node(idd,str(t[2]))
    arbol.edge(ii,idd)
    arbol.edge(ii,t[4])

def p_LCAMPOS2(t):
    '''LCAMPOS : id igual EXP'''
    id = inc()
    t[0] = id
    arbol.node(id,"CAMPO")
    ii = inc()
    arbol.node(ii,"=")
    arbol.edge(id,ii)
    idd = inc()
    arbol.node(idd,str(t[1]))
    arbol.edge(ii,idd)
    arbol.edge(ii,t[3])

def p_DELETE(t):
    '''DELETE : delete   r_from id where LEXP
            | delete  r_from id'''
    id = inc()
    t[0] = id
    arbol.node(id,"delete")
    uno = inc()
    arbol.node(uno,"from ")
    arbol.edge(id,uno)
    iii = inc()
    arbol.node(iii,str(t[3]))
    arbol.edge(uno,iii)
    if len(t) == 6:
        dos = inc()
        arbol.node(dos,"where")
        arbol.edge(id,dos)
        lxpA = t[5]
        for x in range(len(lxpA)):
            arbol.edge(dos,str(lxpA[x]))

def p_EXIST(t):
    '''EXIST : exist para SELECT parc'''
    id = inc()
    t[0] = id
    arbol.node(id,"exist")
    arbol.edge(id,str(t[3]))

def p_LEXP1(t):
    '''LEXP : LEXP coma EXP'''
    t[1].append(t[3])
    t[0] = t[1]

def p_LEXP2(t):
    '''LEXP : EXP'''
    t[0] = [t[1]]

def p_TIPOD(t):
    '''TIPO : decimal para LEXP parc
            | numeric para LEXP parc'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))
    lxpA = t[3]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

def p_TIPOE(t):
    '''TIPO : varchar para int parc
            | timestamp para int parc
            | character para int parc
            | interval para int parc
            | char para int parc
            | time para int parc'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))
    uno = inc()
    arbol.node(uno,str(t[3]))
    arbol.edge(id,uno)

def p_TIPOF(t):
    '''TIPO : character varying para int parc'''
    id = inc()
    t[0] = id
    arbol.node(id,"character varying")
    unp = inc()
    arbol.node(unp,str(t[4]))
    arbol.edge(id,unp)

def p_TIPOG(t):
    '''TIPO : interval cadena'''
    id = inc()
    t[0] = id
    arbol.node(id,str("interval " + t[2]))

def p_TIPOL1(t):
    ''' TIPO : timestamp para int parc without time zone
            | timestamp para int parc with time zone
            | time para int parc without time zone
            | time para int parc with time zone '''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))
    uno = inc()
    arbol.node(uno,str(t[3]))
    arbol.edge(id,uno)
    dos = inc()
    arbol.node(dos,str(t[5] + " time zone"))
    arbol.edge(id,dos)

def p_TIPOL2(t):
    ''' TIPO : interval para int parc cadena '''
    id = inc()
    t[0] = id
    arbol.node(id,"interval")
    uno = inc()
    arbol.node(uno,str(t[3]))
    arbol.edge(id,uno)
    dos = inc()
    arbol.node(dos,str(t[5]))
    arbol.edge(id,dos)

def p_TIPO(t):
    '''TIPO : smallint
            | integer
            | bigint
            | real
            | double precision
            | money
            | text
            | timestamp 
            | date
            | time 
            | interval
            | boolean
            | timestamp without time zone
            | timestamp with time zone
            | time without time zone
            | time with time zone'''
    l = len(t)
    if l == 2:
        id = inc()
        t[0] = id
        arbol.node(id,str(t[1]))
    elif l == 3:
        id = inc()
        t[0] = id
        arbol.node(id,str(t[1] + " " + t[2]))
    elif l == 5:
        id = inc()
        t[0] = id
        arbol.node(id,str(t[1] + " " + t[2] + " " + t[3] + " " + t[4]))


def p_FIELDS(t):
    '''FIELDS : year
        | month
        | day
        | hour
        | minute
        | second'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))


def p_EXP3(t):
    '''EXP : EXP mas EXP
            | EXP menos EXP
            | EXP multiplicacion  EXP
            | EXP division EXP
            | EXP modulo EXP
            | EXP elevado EXP
            | EXP and EXP
            | EXP or EXP
            | EXP mayor EXP
            | EXP menor EXP
            | EXP mayor_igual EXP
            | EXP menor_igual EXP
            | EXP igual EXP
            | EXP diferente1 EXP
            | EXP diferente2 EXP
            | EXP between EXP %prec predicates
            | EXP punto EXP'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[2]))
    arbol.edge(id,str(t[1]))
    arbol.edge(id,str(t[3]))

def p_EXP21(t):
    '''EXP : EXP is not null %prec predicates
            | EXP is not true %prec predicates
            | EXP is not false %prec predicates
            | EXP is not unknown %prec predicates'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[2] + " " + t[3] + " " + t[4]))
    arbol.edge(id,str(t[1]))

def p_EXP22(t):
    '''EXP : EXP is null %prec predicates
            | EXP  is true %prec predicates
            | EXP is unknown %prec predicates
            | EXP as cadena %prec lsel
            | EXP as id %prec lsel
            | EXP as cadenaString %prec lsel
            | EXP is false %prec predicates'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[2] + " " + t[3]))
    arbol.edge(id,str(t[1]))

def p_EXP23(t):
    '''EXP : EXP isnull %prec predicates
            | EXP notnull %prec predicates
            | EXP cadenaString %prec lsel
            | EXP id  %prec lsel
            | EXP cadena %prec lsel'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[2]))
    arbol.edge(id,str(t[1]))
    
def p_EXP1(t):
    '''EXP : mas EXP %prec umas
            | menos EXP %prec umenos
            | not EXP'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[1]))
    arbol.edge(id,str(t[2]))

def p_EXPV1(t):
    '''EXP : EXP not between EXP %prec predicates
            | EXP between symetric EXP %prec predicates'''
    id = inc()
    t[0] = id
    arbol.node(id,str(t[2] + " " + t[3]))
    arbol.edge(id,str(t[1]))
    arbol.edge(id,str(t[4]))

def p_EXPV12(t):
    '''EXP : EXP in para LEXP parc %prec predicates'''
    id = inc()
    t[0] = id
    arbol.node(id,"in")
    arbol.edge(id,str(t[1]))
    lxpA = t[4]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

def p_EXPV2(t):
    '''EXP : EXP not in para LEXP parc %prec predicates'''
    id = inc() 
    t[0] = id
    arbol.node(id,"not in")
    arbol.edge(id,str(t[1]))
    lxpA = t[5]
    for x in range(len(lxpA)):
        arbol.edge(id,str(lxpA[x]))

def p_EXPV3(t):
    '''EXP : EXP is not distinct r_from EXP %prec predicates'''
    id = inc()
    t[0] = id
    arbol.node(id,"is not distinct from")
    arbol.edge(id,str(t[1]))
    arbol.edge(id,str(t[6]))


def p_EXPV32(t):
    '''EXP : EXP is distinct r_from EXP %prec predicates
            | EXP not between symetric EXP %prec predicates'''
    id = inc()
    t[0] = id
    arbol.node(id,(t[2] + " " + t[3] + " " + t[4]))
    arbol.edge(id,str(t[1]))
    arbol.edge(id,str(t[5]))

def p_EXPJ(t):
    '''EXP : SELECT
            | CASE
            | para EXP parc'''
    l = len(t)
    if l == 4:
        t[0] = t[2]
    else:
        t[0] = t[1]

def p_EXP(t):
    '''EXP : id para parc
            | id para LEXP parc
            | any para LEXP parc
            | all para LEXP parc
            | some para LEXP parc
            | extract para FIELDS r_from timestamp cadena parc'''
    l = len(t)
    id = inc()
    t[0] = id
    if l == 4:
        arbol.node(id,str(t[1]+"()"))
    elif l == 5:
        arbol.node(id,str(t[1]))
        lxpA = t[3]
        for x in range(len(lxpA)):
            arbol.edge(id,str(lxpA[x]))
    else:
        arbol.node(id,str(t[1]))
        arbol.edge(id,str(t[3]))
        uno = inc()
        arbol.node(uno,str(t[5]))
        arbol.edge(id,uno)
        dos = inc()
        arbol.node(dos,str(t[6]))
        arbol.edge(id,dos)


def p_EXPT(t):
    '''EXP : int
            | decimales
            | cadena
            | cadenaString
            | true
            | false 
            | id
            | multiplicacion %prec lsel
            | null
            | default
            | current_time
            | current_date
            | timestamp cadena 
            | interval cadena
            | cadena like cadena
            | cadena not like cadena'''
    l = len(t)
    if l == 2:
        id = inc()
        t[0] = id
        arbol.node(id,str(t[1]))
    elif l == 3:
        id = inc()
        t[0] = id
        arbol.node(id,str(t[1] + " " + t[2]))
    elif l == 4:
        id = inc()
        t[0] = id
        arbol.node(id,str(t[1] + " " + t[2], " " + t[3]))
    elif l == 5:
        id = inc()
        t[0] = id
        arbol.node(id,str(t[1] + " " + t[2] + " " + t[3] + " " + t[4]))


def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc

parser = yacc.yacc()

def generarArbol(input):
    r = parser.parse(input)
    arbol.render('ast', view=True)  # doctest: +SKIP
    'ast.pdf'
    return r