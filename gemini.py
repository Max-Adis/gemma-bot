import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class EvitementObstacle(Node):
    def __init__(self):
        super().__init__('Linda ')
        
        # 1. Publier la vitesse (Les muscles)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 70)
        # self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 30)
        
        # 2. S'abonner au LiDAR (Les yeux)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10)
        
        self.get_logger().info("Système d'évitement activé. En route !")

    def scan_callback(self, msg):
        # Le LiDAR envoie 360 rayons. L'index 0 correspond exactement à l'avant du robot.
        distance_avant = msg.ranges[0]
        
        commande = Twist()
        
        # Si un mur est détecté à moins de 0.7 mètre devant
        if distance_avant < 0.7:
            self.get_logger().info(f"Obstacle à {distance_avant:.2f}m ! Je tourne...")
            commande.linear.x = 0.0      # Freinage
            commande.angular.z = 0.6     # Rotation sur place
        else:
            # La voie est libre
            commande.linear.x = 0.2      # Avance tout droit
            commande.angular.z = 0.0     
            
        self.publisher_.publish(commande)

def main(args=None):
    rclpy.init(args=args)
    node = EvitementObstacle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()