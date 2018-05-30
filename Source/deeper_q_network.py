import numpy as np
import networkx as nx
import tensorflow as tf
import random


class DeeperQN():

    def __init__(self, env, n_districts, n_units):
        # Current Network:
        self._n_districts = n_districts
        self._n_units = n_units
        self._env = env

        self._state = tf.placeholder(dtype = tf.float32, shape = [None, n_units, n_districts])
        self._action = tf.placeholder(dtype = tf.float32, shape = [None, n_units * (n_districts - 1)])
        self._state_flat = tf.reshape(self._state, shape = [-1, n_units * n_districts], name = "state_flat")

        self._W_s_1 = tf.get_variable(dtype = tf.float32, shape = [n_units * n_districts, 10], name = "W_s")
        self._W_a_1 = tf.get_variable(dtype = tf.float32, shape = [n_units * (n_districts - 1), 10], name = "W_a")
        self._b_1 = tf.get_variable(dtype = tf.float32, shape = [10], name = "b_1")

        self._h_1 = tf.nn.relu(tf.matmul(self._state_flat, self._W_s_1)  + tf.matmul(self._action, self._W_a_1) + self._b_1)
        self._W_2 = tf.get_variable(dtype = tf.float32, shape = [10, 1], name = "W_2")
        self._b_2 = tf.get_variable(dtype = tf.float32, shape = [1], name = "b_2")

        self._Q_hat = tf.reshape(tf.matmul(self._h_1, self._W_2) + self._b_2, shape = [-1, 1])

        # Target Network:

        self._W_s_1_target = tf.get_variable(dtype=tf.float32, shape=[n_units * n_districts, 10], name="W_s_target")
        self._W_a_1_target = tf.get_variable(dtype=tf.float32, shape=[n_units * (n_districts - 1), 10], name="W_a_target")
        self._b_1_target = tf.get_variable(dtype=tf.float32, shape=[10], name="b_1_target")

        self._h_1_target = tf.nn.relu(
            tf.matmul(self._state_flat, self._W_s_1_target) + tf.matmul(self._action, self._W_a_1_target) + self._b_1_target)
        self._W_2_target = tf.get_variable(dtype=tf.float32, shape=[10, 1], name="W_2_target")
        self._b_2_target = tf.get_variable(dtype=tf.float32, shape=[1], name="b_2_target")

        self._Q_hat_target = tf.reshape(tf.matmul(self._h_1_target, self._W_2_target) + self._b_2_target, shape = [-1, 1])

        self._weights = [self._W_s_1, self._W_a_1, self._b_1, self._W_2, self._b_2]
        self._weights_target = [self._W_s_1_target, self._W_a_1_target, self._b_1_target, self._W_2_target, self._b_2_target]

    def train(self, n_epochs = 10, batch_size = 1, discount = 1, tau = 0.999, lr = 0.1):
        self._replay_buffer = []
        self._y = tf.placeholder(dtype = tf.float32, shape = [None, 1])
        self._sess = tf.Session()
        self._sess.run(tf.global_variables_initializer())

        grad_W_s_1, grad_W_a_1, grad_b_1, grad_W_2, grad_b_2 = tf.gradients(ys = self._Q_hat, xs = self._weights)

        for epoch in range(n_epochs):
            print("Epoch " + str(epoch))
            # Sample action and state
            state = self._env.sample_state()
            (position, displacement) = self._env.sample_action()
            action = self.tuple_to_action(position, displacement)
            new_state = self._env.act(state, (position, displacement))
            reward = self._env.reward(state, (position, displacement))
            self._replay_buffer.append((state, action, new_state, reward))

            # Pop some old sample:
            if len(self._replay_buffer) > 200:
                self._replay_buffer.pop(0)

            # Uniformly sample the replay buffer
            ind = random.randrange(0, len(self._replay_buffer))
            state, action, new_state, reward = self._replay_buffer[ind]

            # Compute the target:
            y = np.array([reward + discount * self.find_best_Q_target_v2(new_state)])
            y = y.reshape(1, 1)


            # Minimize the Bellman error:
            assign_W_s_1 = self._W_s_1.assign(self._W_s_1 - lr * grad_W_s_1 * (self._Q_hat - self._y))
            assign_W_a_1 = self._W_a_1.assign(self._W_a_1 - lr * grad_W_a_1 * (self._Q_hat - self._y))
            assign_b_1 = self._b_1.assign(self._b_1 - tf.reshape(lr * grad_b_1 * (self._Q_hat - self._y), [10]))
            assign_W_2 = self._W_2.assign(self._W_2 - lr * grad_W_2 * (self._Q_hat - self._y))
            assign_b_2 = self._b_2.assign(self._b_2 - tf.reshape(lr * grad_b_2 * (self._Q_hat - self._y), [1]))

            assigns = [assign_W_s_1, assign_W_a_1, assign_b_1, assign_W_2, assign_b_2]

            self._sess.run(assigns, feed_dict = {self._state: [state],
                                                                            self._action: [action],
                                                                            self._y: y})




            # Update the target network using Polyak averaging:
            assign_W_s_1_target = self._W_s_1_target.assign(tau * self._W_s_1_target + (1 - tau) * self._W_s_1)
            assign_W_a_1_target = self._W_a_1_target.assign(tau * self._W_a_1_target + (1 - tau) * self._W_a_1)
            assign_b_1_target = self._b_1_target.assign(tau * self._b_1_target + (1 - tau) * self._b_1)
            assign_W_2_target = self._W_2_target.assign(tau * self._W_2_target + (1 - tau) * self._W_2)
            assign_b_2_target = self._b_2_target.assign(tau * self._b_2_target + (1 - tau) * self._b_2)
            assigns_target = [assign_W_s_1_target, assign_W_a_1_target, assign_b_1_target, assign_W_2_target, assign_b_2_target]

            self._sess.run(assigns_target)
            # print(self._sess.run(self._W_s_1))


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

    # Using double Q:
    def find_best_Q_target_v2(self, state):
        q_list = []
        for ind in range(self._n_units * (self._n_districts - 1)):
            action = np.zeros(self._n_units * (self._n_districts - 1))
            action[ind] = 1
            q = self._sess.run(self._Q_hat, feed_dict = {self._state: [state], self._action: [action]})
            q_list.append(q)

        act_ind = np.argmax(q_list)
        action = np.zeros(self._n_units * (self._n_districts - 1))
        action[act_ind] = 1
        return self._sess.run(self._Q_hat_target, feed_dict = {self._state: [state], self._action: [action]})


    def act(self, state):
        q_list = []
        for ind in range(self._n_units * (self._n_districts - 1)):
            action = np.zeros(self._n_units * (self._n_districts - 1))
            action[ind] = 1
            q = self._sess.run(self._Q_hat, feed_dict = {self._state: [state], self._action: [action]})
            q_list.append(q)

        act_ind = np.argmax(q_list)
        displacement = act_ind % (self._n_districts - 1) + 1
        position = act_ind // (self._n_districts - 1)
        return (position, displacement)




