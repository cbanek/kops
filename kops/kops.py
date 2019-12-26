from kubernetes import client, config

from app import Application

config.load_kube_config()
App = Application().run()
