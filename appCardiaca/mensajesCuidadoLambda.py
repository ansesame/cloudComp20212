import boto3
import random

def lambda_handler(event, context):
    
    asunto = 'Notas para el cuidado del corazón'
    mensaje = ['Realiza actividad física y evita el sedentarismo',
        'Bebe agua para mantenerte bien hidratado',
        'Aumenta las porciones de frutas, verduras y fibra',
        'Realiza pausas activas para que tu corazón sea cada vez más saludable',
        'Evita el cigarrillo y controla el consumo de alcohol',
        'Mantente en forma y controla tu peso',
        'Que no se te olvide dormir bien',
        'No olvides realizarte chequeos constantes con tu médico'
        ]
    
    # Enviar mensaje a SNS
    MY_SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:150839082595:proyecto4_AndresSalazar'
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn = MY_SNS_TOPIC_ARN,
        Subject = asunto,
        Message = random.choice(mensaje)
    )
    return('Mensaje enviado')
