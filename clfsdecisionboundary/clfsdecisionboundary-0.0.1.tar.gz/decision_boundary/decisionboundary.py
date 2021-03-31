import numpy as np
import matplotlib.pyplot as plt
def two_features_plot_decision_boundary(model, X, y):
  import numpy as np
  import matplotlib.pyplot as plt

  x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
  y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
  xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                       np.linspace(y_min, y_max, 100))
  

  x_in = np.c_[xx.ravel(), yy.ravel()] 

  y_pred = model.predict(x_in)


  if len(y_pred[0]) > 1:
    print("MultiClass Classification")
    # We have to reshape our predictions to get them ready for plotting
    y_pred = np.argmax(y_pred, axis=1).reshape(xx.shape)
  else:
    print("Binary Classification")
    y_pred = np.round(y_pred).reshape(xx.shape)
  
  # Plot decision boundary
  plt.contourf(xx, yy, y_pred, cmap=plt.cm.RdYlBu, alpha=0.7)
  plt.scatter(X[:, 0], X[:, 1], c=y, s=40, cmap=plt.cm.PiYG)
  plt.xlim(xx.min(), xx.max())
  plt.ylim(yy.min(), yy.max())


def two_features_plot_decision_boundary_ml(model, X, y):
  import numpy as np
  import matplotlib.pyplot as plt

  x_min, x_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
  y_min, y_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
  xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                       np.linspace(y_min, y_max, 100))
  

  x_in = np.c_[xx.ravel(), yy.ravel()] 

  y_pred = model.predict(x_in)


  if len(np.unique(y_pred)) > 2:
    print("MultiClass Classification")
    # We have to reshape our predictions to get them ready for plotting
    y_pred = np.argmax(y_pred, axis=1).reshape(xx.shape)
  else:
    print("Binary Classification")
    y_pred = np.round(y_pred).reshape(xx.shape)
  
  # Plot decision boundary
  plt.contourf(xx, yy, y_pred, cmap=plt.cm.RdYlBu, alpha=0.7)
  plt.scatter(X[:, 0], X[:, 1], c=y, s=40, cmap=plt.cm.PiYG)
  plt.xlim(xx.min(), xx.max())
  plt.ylim(yy.min(), yy.max())