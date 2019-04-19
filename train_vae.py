# coding: utf-8

import pickle,random,os,time
import model as vcgan
#import scipy.io as sio
#import tensorflow as tf

#from utils import *
#from test_utils import *
import numpy as np
import utils
import test_utils

def train_VAE(_model):
#    dataname_a = _model.dataset_name_a
#    featurefile_a = './'+dataname_a+'.mat'
#    resultmax = 0.95
#    resultmin = -0.95
#    useS = True
#    feature_a, neighbour1_a, degree1_a, logrmin_a, logrmax_a, smin_a, smax_a, modelnum_a, \
#        pointnum1_a, maxdegree1_a, L1_a, cotw1_a = utils.load_data(featurefile_a, resultmin, resultmax, useS=useS)
#    self.feature_a, self.neighbour1_a, self.degree1_a, self.logrmin_a, self.logrmax_a, self.smin_a, self.smax_a, self.modelnum_a, \
#        self.pointnum1_a, self.maxdegree1_a, self.L1_a, self.cotw1_a = utils.load_data(featurefile_a, resultmin, resultmax, useS=useS)
        
#    Ilf = np.zeros((_model.batch_size, 1))
    rng = np.random.RandomState(23456)

#    if False:
    if os.path.isfile("id.dat"):
        id = pickle.load(open('id.dat', 'rb'))
        id.show()
        Ia = id.Ia
#        Ib = id.Ib
    else:
        Ia = np.arange(len(_model.feature_a))
#        Ib = np.arange(len(_model.feature_b))
        Ia = random.sample(list(Ia), int(len(_model.feature_a) * (1 - vcgan.vae_ablity)))
#        Ib = random.sample(list(Ib), int(len(_model.feature_b) * (1 - vcgan.vae_ablity)))
#        id = Id(Ia, Ib)
        id = utils.Id(Ia)
        #id.show()
        f = open('id.dat', 'wb')
        pickle.dump(id, f, 0)
        f.close()
        id = pickle.load(open('id.dat', 'rb'))
        id.show()

    _model.file.write("VAE start\n")
#    for step in xrange(_model.start_step_vae, vcgan.n_epoch_Vae):
    for step in range(_model.start_step_vae, vcgan.n_epoch_Vae):
        rng.shuffle(Ia)
#        rng.shuffle(Ib)
#        train each batch
        for i in range(0, len(Ia), _model.batch_size):
            timeserver1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            feature_a = _model.feature_a[Ia[i:i+_model.batch_size]]
            random_a = utils.gaussian(len(feature_a), _model.hidden_dim)
            _, cost_generation_a, cost_latent_a, l2_loss_a = _model.sess.run(
                    [_model.train_op_vae_a, _model.neg_loglikelihood_a, _model.KL_divergence_a, _model.r2_a],
                    feed_dict={_model.inputs_a: feature_a, _model.random_a: random_a})
            print("%s Processed %d|%d" % (timeserver1, i+_model.batch_size, len(Ia)))
        
        timeserver1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print("|%s step: [%2d|%d]cost_generation_a: %.8f, cost_latent_a: %.8f, l2_loss_a: %.8f" % (
                timeserver1, step + 1, vcgan.n_epoch_Vae, cost_generation_a, cost_latent_a, l2_loss_a))
        
#        feature_a = _model.feature_a[Ia]
##        feature_b = _model.feature_b[Ib]
#        random_a = utils.gaussian(len(feature_a), _model.hidden_dim)
##        random_b = gaussian(len(feature_b), _model.hidden_dim)
#
#        # ------------------------------------VAE a
#        _, cost_generation_a, cost_latent_a, l2_loss_a = _model.sess.run(
#            [_model.train_op_vae_a, _model.neg_loglikelihood_a, _model.KL_divergence_a, _model.r2_a],
#            feed_dict={_model.inputs_a: feature_a, _model.random_a: random_a})
#        print("|%s step: [%2d|%d]cost_generation_a: %.8f, cost_latent_a: %.8f, l2_loss_a: %.8f" % (
#            timeserver1, step + 1, vcgan.n_epoch_Vae, cost_generation_a, cost_latent_a, l2_loss_a))
##        # ------------------------------------VAE b
##        _, cost_generation_b, cost_latent_b, l2_loss_b = _model.sess.run(
##            [_model.train_op_vae_b, _model.neg_loglikelihood_b, _model.KL_divergence_b, _model.r2_b],
##            feed_dict={_model.inputs_b: feature_b, _model.random_b: random_b})
##        print("|%s step: [%2d|%d]cost_generation_b: %.8f, cost_latent_b: %.8f, l2_loss_b: %.8f" % (
##            timeserver1, step + 1, vcgan.n_epoch_Vae, cost_generation_b, cost_latent_b, l2_loss_b))

        _model.file.write("|%s Epoch: [%5d|%d] cost_generation_a: %.8f, cost_latent_a: %.8f, l2_loss_a: %.8f\n" \
                        % (timeserver1, step + 1, vcgan.n_epoch_Vae, cost_generation_a, cost_latent_a, l2_loss_a))

#        _model.file.write("|%s Epoch: [%5d|%d] cost_generation_b: %.8f, cost_latent_b: %.8f, l2_loss_b: %.8f\n" \
#                        % (timeserver1, step + 1, vcgan.n_epoch_Vae, cost_generation_b, cost_latent_b, l2_loss_b))

        _model.file_vae.write("A %d %.8f %.8f %.8f\n" % (step + 1, cost_generation_a, cost_latent_a, l2_loss_a))
#        _model.file_vae.write("B %d %.8f %.8f %.8f\n" % (step + 1, cost_generation_b, cost_latent_b, l2_loss_b))

        if vcgan.tb and (step + 1) % 20 == 0:
#            s = _model.sess.run(_model.merge_summary,
#                              feed_dict={_model.inputs_a: feature_a, _model.inputs_b: feature_b,
#                                         _model.random_a: random_a,
#                                         _model.random_b: random_b, _model.lf_dis: Ilf})
            s = _model.sess.run(_model.merge_summary,
                              feed_dict={_model.inputs_a: feature_a,
                                         _model.random_a: random_a})
            _model.write.add_summary(s, step)

        if (step + 1) % 10 == 0:
            print('Saving model...\n')
#            print(vcgan.logfolder)
#            if vcgan.test_vae:
#                test_utils.test_vae(_model, step)
            save_path = _model.saver_vae_a.save(_model.sess, _model.checkpoint_dir_vae_a + '/vae_a.model', global_step=step + 1)
            print("Model saved in path: %s" % save_path)
            
            # self.saver_vae_b.save(self.sess, self.checkpoint_dir_vae_b + '/vae_b.model', global_step=step + 1)
#            _model.saver_vae_all.save(_model.sess, _model.checkpoint_dir_vae_all + '/vae_all.model', global_step=step + 1)
    print('---------------------------------train VAE success!!----------------------------------')
#    print('------------------------------------train Metric--------------------------------------')
    # self.save(sess, self.checkpoint_dir, n_iteration)



