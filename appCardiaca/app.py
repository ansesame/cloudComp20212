# -*- coding: utf-8 -*-

import pandas as pd
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import os
import re
import boto3

# Función para verificar un correo valido
def checkEmail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}[.]?\w{0,3}$'
    return re.search(regex,email)

# Función para realizar suscripción a sns
session = boto3.Session(region_name='us-east-1')
MY_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:150839082595:proyecto4_AndresSalazar'
sns_client = session.client('sns')

def suscribirTemaSNS(email):
    response = sns_client.subscribe(
        TopicArn = MY_SNS_TOPIC_ARN,
        Protocol = 'email',
        Endpoint = email
    )
    print(response)

# Importar datos
os.system('kaggle datasets download ronitf/heart-disease-uci --unzip')

# Obtener datos
data = pd.read_csv('heart.csv')

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

mensajeSuscripcion = 'Suscribase a nuestra lista de correos para \
recibir recomendaciones diarias sobre el cuidado del corazón.'

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

suscripcion = html.Div([
                        html.P(children=[mensajeSuscripcion],
                               className='four columns'
                               ),
                        html.Div(dcc.Input(id='input-on-submit',
                                           type='text',
                                           style={'width': '95%'}
                                           ),
                                 className='three columns',
                                 style={'marginLeft': '10px',
                                        'display': 'flex',
                                        'justifyContent': 'center',
                                        'alignItems': 'center'
                                        }
                                 ),
                        html.Div(html.Button('Suscribirse',
                                             id='submit-val',
                                             n_clicks=0,
                                             style={'margin': '0',
                                                    'padding': '0',
                                                    'textAlign': 'center',
                                                    'width': '95%',
                                                    'backgroundColor': '#b8c0ff' 
                                                    }
                                             ),
                                 className='two columns',
                                 style={'marginLeft': '10px'}
                                 ),
                        html.Div(id='container-button-basic',
                                 children=' ',
                                 className='three columns'
                                 )
                        ],
                       style={'margin': '20px 2% 0 2%',
                              'border': '2px #119dff solid',
                              'borderRadius': '10px',
                              'padding': '5px'
                              },
                       className='row'
                       )

# Contenido
app.layout = html.Div(children=[
    html.Div([titulo], style={'marginLeft': '2%'}),
    html.Div([introduccion], style={'marginLeft': '2%'}),
    suscripcion,
    html.Div( [dcc.Tabs([grafica1, grafica2, grafica3])] ,
              style={'margin': '15px 2% 2% 2%',
                     'backgroundColor':'white',
                    })
    ],
    style={'backgroundColor':'#e6e9ff',
        'width':'100%', 'height':'auto',
        'margin':'-1% 0 0 0'
    }
)

# Funcionalidad
@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    if type(value) == str:
        if checkEmail(value):
            try:
                suscribirTemaSNS(value)
            except:
                return 'Error al suscribir correo'
            
            return 'Se ha solicitado la suscripción del correo "' \
                + value +'", revise su bandeja para confirmar'
        else:
            return 'Dirección de correo inválida'
    else:
        return ' '


# Titulo tab
app.title = 'Detección Temprana'

if __name__ == '__main__':
    app.run_server(debug=True)
