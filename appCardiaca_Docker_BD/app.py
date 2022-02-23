# -*- coding: utf-8 -*-

import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px
import psycopg2

# Conexión BD
conn = psycopg2.connect(
    dbname="deteccion_temprana",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)

# Obtener datos necesarios
query = 'SELECT target, cp, trestbps, thalach FROM heart_obs;'
data = pd.read_sql_query(query, conn)
print(data.dtypes)
# Crear servidor
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Gráficas
fig1 = px.imshow( pd.crosstab(data.target, data.cp),
               labels=dict(y="Presenta enfermedad",
                           x="Tipo de dolor en el pecho",
                           color="# individuos"),
               y=['0', '1'], x = ['0  ','1  ','2  ','3  '],
               color_continuous_scale='viridis')
textofig11 = '''
En la presente figura se compara la incidencia de diferentes \
tipos de dolor en el pecho y la presencia de alguna enfermedad cardiovascular \
en el paciente: 1, presenta; 0, no presenta. 
De esta gráfica podemos notar que:
'''
textofig12 = '''
- El tipo de dolor 0 es el dolor más común para las personas que no presentan \
afectación cardíaca. Pero los tipos de dolor 1, 2 y 3 se vuelven de \
mayor frecuencia ante la presencia de enfermedad, con una incidencia \
varias veces mayor que en los individuos sanos.
'''
textofig13 = '''
Con lo anterior se sugiere que el tipo de dolor 0 es indicativo de un \
paciente sano, lo contrario ocurre para los tipos de dolor 1, 2 y 3
'''

fig2 = px.box(data, x='target', y='trestbps', points='all',
            labels={'target': 'Presenta enfermedad',
                    'trestbps': 'Presión arterial en reposo (mm HG)'
                   })
textofig21 = 'En cuanto a la presión arterial en reposo, comparada en \
esta figura, se encuentra que tanto individuos sanos como enfermos tienen \
una distribución similar. Ambos tipos de individuo comparten una mediana de \
130 mm HG, así como un recorrido intercuantílico similar.'
textofig22 = 'Además, la presencia de valores atípicos altos en individuo sanos \
debe deberse a que estos conforman una muestra más grande. Con lo que se \
concluye que esta variable no aporta a la detección enfermedades cardíacas.'

fig3 = px.histogram(data, x='thalach', color='target',  marginal='violin',
                  labels={'target': 'Enfermedad',
                          'thalach': 'Frecuencia cardíaca máxima (mm HG)',
                         },
                  opacity=0.7)
fig3.update_layout(yaxis_title="Frecuencia")
textofig31 = 'La variable explorada aquí es la frecuencia cardíaca máxima, \
que indica el mayor número alcanzado de pulsaciones del corazón por minuto. \
Luego, la presente figura muestra que la distribución de esta variable se ve \
afectada por la presencia de enfermedad. Al pasar el cursos por la gráfica \
superior se ve que la mediana de una persona sana está en 142 mmHG, mientras \
que para un individuo enfermo es mayor por casi 20 mmHG.'
textofig32 = 'Con esto se puede sugerir que entre mayor sea la frecuencia \
cardíaca máxima, mayor será la probabilidad de que el individuo presente \
una enfermedad cardíaca.'

# Introducción
textoIntro = 'Según el Centro para el Control y la Prevención de \
Enfermedades, CDC, cada minuto una persona en los Estados Unidos muere \
de un episodio relacionado con una enfermedad cardiaca. Sin embargo, en muchos \
casos la detección temprana permite enfrentar la enfermedad en su \
etapa más temprana y tratable, permitiendo mitigar el riesgo de los pacientes. \
Por tanto, con el proposito de brindar ayuda a los profesionales de la salud, \
se inspeccionan a continuación diferentes variables que permitan \
distinguir la presencia estas enfermedades. Los datos usados corresponden \
a la Cleveland database publicada en '

# Componentes del tablero
titulo = html.H3(children='Detección temprana de enfermedades cardíacas')
introduccion = html.P(children=[textoIntro,
                                dcc.Link('Kaggle.',
                                         href='https://www.kaggle.com/ronitf/heart-disease-uci'
                                )
                                ]
                      )

grafica1 = dcc.Tab(label='Tipo de dolor',
                   children=[
                       dcc.Graph( id='graph1', figure=fig1,
                                  className='eight columns',
                                  style={'height':'60vh'}
                       ),
                       html.Div(children=[textofig11, html.Br(),
                                          textofig12, html.Br(),
                                          html.Br(), textofig13
                                          ],
                                className='four columns',
                                style={'margin': '15px 2px 5px 0'}
                                )
                   ],
                   className='row'
                   )
grafica2 = dcc.Tab(label='Presión arterial en reposo',
                   children=[
                       dcc.Graph( id='graph2', figure=fig2,
                                  className='eight columns',
                                  style={'height':'60vh'}
                       ),
                       html.Div(children=[textofig21, html.Br(),
                                          html.Br(), textofig22
                                         ],
                                className='four columns',
                                style={'margin': '15px 2px 5px 0'}
                                )
                   ],
                   className='row'
                   )
grafica3 = dcc.Tab(label='Frecuencia cardíaca máxima',
                   children=[
                       dcc.Graph( id='graph3', figure=fig3,
                                  className='eight columns',
                                  style={'height':'60vh'}
                       ),
                       html.Div(children=[textofig31, html.Br(),
                                          html.Br(), textofig32
                                         ],
                                className='four columns',
                                style={'margin': '15px 2px 5px 0'}
                                )
                   ],
                   className='row'
                   )

# Contenido
app.layout = html.Div(children=[
    html.Div([titulo], style={'marginLeft': '2%'}),
    html.Div([introduccion], style={'marginLeft': '2%'}),
    html.Div( [dcc.Tabs([grafica1, grafica2, grafica3])] ,
              style={'margin': '15px 2% 2% 2%',
                     'backgroundColor':'white',
                    })
    ],
    style={'backgroundColor':'#e6e9ff',
        'width':'100%', 'height':'100vh',
        'margin':'-1% 0 0 0'
    }
)
# Titulo tab
app.title = 'Detección Temprana'

if __name__ == '__main__':
    app.run_server(debug=True)
