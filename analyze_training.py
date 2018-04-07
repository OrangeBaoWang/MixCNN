import sys
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle

# Set the default color cycle
#mpl.rcParams['axes.color_cycle'] = ['r', 'k', 'c']
sns.set_palette(sns.color_palette("GnBu_d"))
#"PuBuGn_d"

def analyze(filepath):
	# load training history 
	training_history = pickle.load(open(filepath, "rb"))
	date_and_time = filepath.split('/')[len(filepath.split('/'))-2]

	# create training loss plot - over all epochs
	fig1 = plt.figure()
	for i, fold in training_history.items():
		loss = fold['loss']
		val_loss = fold['val_loss']

		n_epochs = len(loss)

		t = np.arange(1, n_epochs+1)
		ax1 = fig1.add_subplot(2, 1, 1)
		ax1.plot(t, loss, linewidth=1.0)
		ax1.set_ylabel('Training Loss (MSE)')
		ax1.set_title('Training Loss (MSE)')

		ax2 = fig1.add_subplot(2, 1, 2)
		ax2.plot(t, val_loss, linewidth=1.0)
		ax2.set_xlabel('Epoch')
		ax2.set_ylabel('Validation Loss (MSE)')

	fig1.savefig(os.path.join("reports", date_and_time, "train_and_val_loss_summary.png"))

	# create training loss plot - over ending epochs
	fig2 = plt.figure()
	for i, fold in training_history.items():
		loss = fold['loss']
		val_loss = fold['val_loss']

		n_epochs = len(loss)
		start = n_epochs-(int(np.floor(0.5*n_epochs)))
		end = n_epochs

		t = np.arange(start, end)
		ax1 = fig2.add_subplot(2, 1, 1)
		ax1.plot(t, loss[start:end], linewidth=0.5)
		ax1.set_ylabel('Training Loss (MSE)')
		ax1.set_title('Training Loss (MSE)')

		ax2 = fig2.add_subplot(2, 1, 2)
		ax2.plot(t, val_loss[start:end], linewidth=0.5)
		ax2.set_xlabel('Epoch')
		ax2.set_ylabel('Validation Loss (MSE)')

	fig2.savefig(os.path.join("reports", date_and_time, "train_and_val_loss_end_epochs_summary.png"))

	# create training loss plots over ending epochs for each fold
	if not os.path.isdir(os.path.join("reports", date_and_time, "all_folds")):
		os.makedirs(os.path.join("reports", date_and_time, "all_folds"))

	for i, fold in training_history.items():
		loss = fold['loss']
		val_loss = fold['val_loss']

		n_epochs = len(loss)
		start = n_epochs-(int(np.floor(0.5*n_epochs)))
		end = n_epochs

		t = np.arange(start, end)
		fig3 = plt.figure()
		ax1 = fig3.add_subplot(2, 1, 1)
		ax1.plot(t, loss[start:end], linewidth=0.5)
		ax1.set_ylabel('Training Loss (MSE)')
		ax1.set_title('Training Loss (MSE) for Fold {0}'.format(i+1))

		ax2 = fig3.add_subplot(2, 1, 2)
		ax2.plot(t, val_loss[start:end], linewidth=0.5)
		ax2.set_xlabel('Epoch')
		ax2.set_ylabel('Validation Loss (MSE)')

		fig3.savefig(os.path.join("reports", date_and_time, "all_folds", "train_and_val_loss_fold{0}_summary.png".format(i+1)))

if __name__ == "__main__":
	if len(sys.argv) == 2:
		filepath = sys.argv[1]
		analyze(filepath)
	else:
		print("Invalid training history file.")