# Machine Learning Concepts

## Supervised vs Unsupervised Learning
Supervised learning uses labeled data to train models that predict outcomes. Examples include classification tasks like spam detection and regression tasks like house price prediction. Common algorithms are linear regression, decision trees, random forests, and neural networks. Unsupervised learning finds patterns in unlabeled data. Clustering algorithms like K-means group similar data points, while dimensionality reduction techniques like PCA reduce the number of features while preserving important information.

## Overfitting and Underfitting
Overfitting occurs when a model learns the training data too well, including its noise, and performs poorly on new unseen data. Signs include very high training accuracy but low test accuracy. Solutions include using more training data, adding regularization, using dropout in neural networks, and simplifying the model. Underfitting occurs when a model is too simple to capture the underlying patterns. Signs include poor performance on both training and test data. Solutions include using a more complex model, adding features, or training longer.

## Cross-Validation
Cross-validation is a technique for evaluating model performance more reliably than a simple train-test split. In k-fold cross-validation, the data is divided into k equal parts. The model is trained k times, each time using k-1 folds for training and the remaining fold for testing. The final performance is the average across all k runs. This gives a more robust estimate of how the model will perform on unseen data. Common choices are 5-fold or 10-fold cross-validation.

## Feature Engineering
Feature engineering is the process of creating new input features from existing data to improve model performance. Techniques include one-hot encoding for categorical variables, normalization and standardization for numerical features, creating interaction features by combining existing ones, and extracting date components like day of week or month. Good feature engineering often has a bigger impact on model performance than choosing a more complex algorithm.

## Neural Networks and Deep Learning
Neural networks are computing systems inspired by biological neural networks. They consist of layers of interconnected nodes that process information. A basic network has an input layer, one or more hidden layers, and an output layer. Deep learning refers to neural networks with many hidden layers. Popular architectures include Convolutional Neural Networks for images, Recurrent Neural Networks for sequences, and Transformers for natural language processing. Training uses backpropagation and gradient descent to adjust the weights.

## Model Evaluation Metrics
Different tasks require different evaluation metrics. For classification, accuracy measures overall correctness, precision measures the proportion of positive predictions that are correct, recall measures the proportion of actual positives that are found, and F1-score is the harmonic mean of precision and recall. For regression, common metrics are Mean Squared Error, Root Mean Squared Error, and R-squared score. Choosing the right metric depends on the business problem and the cost of different types of errors.
