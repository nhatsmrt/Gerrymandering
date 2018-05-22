import numpy as np
import networkx as nx
import tensorflow as tf
import random


class DQN():

    def __init__(self, env, n_districts, n_units):
        # Current Network:
        self._n_districts = n_districts
        self._n_units = n_units
        self._env = env

        self._state = tf.placeholder(dtype = tf.float32, shape = [None, n_units, n_districts])
        self._action = tf.placeholder(dtype = tf.float32, shape = [None, n_units * (n_districts - 1)])
        self._state_flat = tf.reshape(self._state, shape = [-1, n_units * n_districts], name = "state_flat")

        self._W_s = tf.get_variable(dtype = tf.float32, shape = [n_units * n_districts, 1], name = "W_s")
        self._W_a = tf.get_variable(dtype = tf.float32, shape = [n_units * (n_districts - 1), 1], name = "W_a")
        self._b = tf.get_variable(dtype = tf.float32, shape = [1], name = "b")

        self._Q_hat = tf.matmul(self._state_flat, self._W_s)  + tf.matmul(self._action, self._W_a) + self._b

        # Target Network:

        self._W_s_target = tf.get_variable(dtype = tf.float32, shape = [n_units * n_districts, 1], name = "W_s_target")
        self._W_a_target = tf.get_variable(dtype = tf.float32, shape = [n_units * (n_districts - 1), 1], name = "W_a_target")
        self._b_target = tf.get_variable(dtype = tf.float32, shape = [1], name = "b_target")

        self._Q_hat_target = tf.matmul(self._state_flat, self._W_s_target)  + tf.matmul(self._action, self._W_a_target) + self._b_target




    def train(self, n_epochs = 10, batch_size = 1, discount = 1, tau = 0.999, lr = 0.1):
        self._replay_buffer = []
        self._y = tf.placeholder(dtype = tf.float32, shape = [1])
        self._sess = tf.Session()
        self._sess.run(tf.global_variables_initializer())

        # opt = tf.train.AdamOptimizer()
        # grad = opt.compute_gradients(self._Q_hat_target, var_list = [self._W_s, self._W_a, self._b])
        grad_W_s, grad_W_a, grad_b = tf.gradients(ys = self._Q_hat, xs = [self._W_s, self._W_a, self._b])

        for epoch in range(n_epochs):
            # Sample action and state
            state = self._env.sample_state()
            (position, displacement) = self._env.sample_action()
            action = self.tuple_to_action(position, displacement)
            new_state = self._env.act(state, (position, displacement))
            reward = self._env.reward(state, (position, displacement))
            self._replay_buffer.append((state, action, new_state, reward))

            # Uniformly sample the replay buffer
            ind = random.randrange(0, len(self._replay_buffer))
            state, action, new_state, reward = self._replay_buffer[ind]

            # Compute the target:
            y = reward + discount * self.find_best_Q_target(new_state)


            # Minimize the Bellman error:
            assign_W_s = self._W_s.assign(lr * grad_W_s * (self._Q_hat - self._y))
            assign_W_a = self._W_a.assign(lr * grad_W_a * (self._Q_hat - self._y))
            assign_b = self._b.assign(tf.reshape(lr * grad_b * (self._Q_hat - self._y), [1]))
            self._sess.run([assign_W_s, assign_W_a, assign_b], feed_dict = {self._state: [state],
                                                                            self._action: [action],
                                                                            self._y: [y]})




            # Update the target network using Polyak averaging:
            assign_W_s_target = self._W_s_target.assign(tau * self._W_s_target + (1 - tau) * self._W_s)
            assign_W_a_target = self._W_a_target.assign(tau * self._W_a_target + (1 - tau) * self._W_a)
            assign_b_target = self._b_target.assign(tau * self._b_target + (1 - tau) * self._b)
            self._sess.run([assign_W_s_target, assign_W_a_target, assign_b_target])


        print("Finish Training")

    def tuple_to_action(self, position, displacement):
        action = np.zeros(self._n_units * (self._n_districts - 1))
        action[position * (self._n_districts - 1) + displacement - 1] = 1
        return action


    def find_best_Q_target(self, state):
        q_list = []
        for ind in range(self._n_units * (self._n_districts - 1)):
            action = np.zeros(self._n_units * (self._n_districts - 1))
            action[ind] = 1
            q = self._sess.run(self._Q_hat_target, feed_dict = {self._state: [state], self._action: [action]})
            q_list.append(q)

        return np.max(q_list)

    def act(self, state):
        q_list = []
        for ind in range(self._n_units * (self._n_districts - 1)):
            action = np.zeros(self._n_units * (self._n_districts - 1))
            action[ind] = 1
            q = self._sess.run(self._Q_hat, feed_dict = {self._state: state, self._action: action})
            q_list.append(q)

        return np.argmax(q_list)




