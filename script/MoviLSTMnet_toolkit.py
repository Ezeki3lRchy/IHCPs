import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import logging

def csv_generator(env_var):
    """
    Generates a CSV file containing information about input and output folder pairs.
    """
    import logging

    # Set specific logger for this function
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)  # 强制设置级别为 WARNING

    # Define input and output directory paths
    input_path = os.path.join(env_var, 'input')
    output_path = os.path.join(env_var, 'output')

    # Check if both input and output paths exist
    if not os.path.isdir(input_path) or not os.path.isdir(output_path):
        logging.error("Either 'input' or 'output' directory does not exist.")
        return

    data = []  # Initialize the data list to store folder details

    # Iterate over folders in the input path, sorted for consistency
    for folder_name in sorted(os.listdir(input_path)):
        input_folder = os.path.join(input_path, folder_name)
        output_folder = os.path.join(output_path, folder_name)

        # Check if corresponding input and output folders exist
        if os.path.isdir(input_folder) and os.path.isdir(output_folder):
            logging.info(f"Processing folder: {folder_name}")  # INFO 不会输出
            data.append({
                'folder_name': folder_name,
                'input_folder': input_folder,
                'output_folder': output_folder
            })
        else:
            logging.warning(
                f"Skipping folder: {folder_name} - "
                f"Missing corresponding input or output directory."
            )

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Define the output CSV file path
    csv_path = os.path.join(env_var, 'dataset_info.csv')

    # Save the DataFrame to a CSV file
    try:
        df.to_csv(csv_path, index=False)
        logging.info(f"CSV file generated successfully: {csv_path}")  # INFO 不会输出
    except Exception as e:
        logging.error(f"Failed to save CSV: {e}")





# Function to plot model history from a DataFrame
def plotModelHistoryFromFile_MSE(history_df, fig_initial_value=1, save_fig=False, file_name=None, fig_vars=None):
    fig, ax = plt.subplots(1, 2, figsize=(15, 4))

    fontsize_label = 12
    
    # Extract keys from DataFrame columns
    keys = history_df.columns
    
    # Plot settings: each tuple contains (training variable, validation variable, plot title)
    # Default plot variables if not provided
    if fig_vars is None:
        fig_vars = [
            ('loss', 'val_loss', "Train loss vs Validation loss"),
            ('mean_squared_error', 'val_mean_squared_error', "Train MSE vs Validation MSE")
        ]
    
    # Number of epochs (assuming epochs start from fig_initial_value)
    epochs = range(fig_initial_value, fig_initial_value + len(history_df['loss']))
    
    # Iterate over the plot settings and plot each subplot
    for i, (train_var, val_var, title) in enumerate(fig_vars):
        if train_var in keys and val_var in keys:
            ax[i].semilogy(epochs, history_df[train_var], label=train_var)
            ax[i].semilogy(epochs, history_df[val_var], label=val_var)
            ax[i].legend(fontsize=fontsize_label)
            ax[i].set_title(title, fontsize=fontsize_label)
            
            # Additional settings for the subplot
            for spine in ax[i].spines.values():
                spine.set_linewidth(2)
            ax[i].tick_params(direction='in', which='both')
            ax[i].grid(which='both', linestyle='--', linewidth=0.5)
            ax[i].set_xlabel('Epoch', fontsize=fontsize_label)
            ax[i].set_ylabel(ax[i].get_ylabel(), fontsize=fontsize_label)
        else:
            print(f"Warning: {train_var} or {val_var} not found in DataFrame columns.")

    fig.tight_layout()  # Ensure subplots do not overlap
    plt.show()
    
    # Save the figure if required
    if save_fig:
        if file_name is None:
            # Generate a default file name with a timestamp if none is provided
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'res_{timestamp}.png'
        fig.savefig(file_name, dpi=300)
        print(f"Figure saved as {file_name}")

    # Print max MSE values
    if 'loss' in keys and 'val_loss' in keys:
        print("Max. Training MSE:", max(history_df['loss']))
        print("Max. Validation MSE:", max(history_df['val_loss']))
    else:
        print("Warning: mean_squared_error or val_mean_squared_error not found in DataFrame columns.")
    
    # Print all history keys and values
    #print("Columns:", keys)
    #for key in keys:
    #    print(f"{key}:", history_df[key].values)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoMinorLocator, LogLocator
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

# Define the path to the Times New Roman font on Windows
#font_properties = FontProperties(fname='/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf')

TICK_LABEL_SIZE = 16  # Increased tick label size

# Update rcParams to use Times New Roman for all text elements
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman'] + rcParams['font.serif']
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.rm'] = 'Times New Roman'


#save_path = 'E:\\Project\\cross-sectional project'

def apply_plot_formatting(x_label='x', 
                          y_label='y', 
                          title='title', 
                          font_properties=FontProperties(fname='/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf') # type: ignore
                          ):
    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    if title:
        plt.title(title, fontsize=20)
    plt.legend(fontsize=16, 
               frameon=True, 
               framealpha=1, 
               edgecolor='black', 
               fancybox=False,
               borderpad=0.3, labelspacing=0.2
               )
    plt.grid(which='both', linestyle='--', linewidth=1)  # Set grid lines to be dashed

    # Set the linewidth of the x and y axes
    plt.gca().spines['top'].set_linewidth(2)
    plt.gca().spines['bottom'].set_linewidth(2)
    plt.gca().spines['left'].set_linewidth(2)
    plt.gca().spines['right'].set_linewidth(2)

    # Enable minor ticks
    plt.gca().minorticks_on()
    # Automatically adjust minor ticks to have one minor tick between each pair of major ticks on x-axis
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))


    # Set minor ticks for y-axis on a logarithmic scale
    plt.gca().yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=10))

    # Set font properties for tick labels and make ticks inline
    plt.gca().tick_params(axis='both', which='major', direction='in', length=6, width=1.5, pad=5)
    plt.gca().tick_params(axis='both', which='minor', direction='in', length=3, width=1, pad=5)
    plt.gca().tick_params(axis='x', which='both', top=True, bottom=True)
    plt.gca().tick_params(axis='y', which='both', left=True, right=True)

    for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
        label.set_fontproperties(font_properties)
        label.set_fontsize(TICK_LABEL_SIZE)  # Set the font size for tick labels


def ResizeImage(image, target_height, target_width):
    """
    Resize the image to the target dimensions.

    Parameters:
        image (numpy.ndarray): The input image to be resized.
        target_height (int): The target height for the resized image.
        target_width (int): The target width for the resized image.

    Returns:
        numpy.ndarray: The resized image.
    """
    # Resize the image to the target dimensions with anti-aliasing and 'reflect' mode
    image_resized = resize(image, (target_height, target_width), 
                           anti_aliasing=True, 
                           mode='reflect')  # 'reflect' mode reflects the last few pixels at the border
    
    return image_resized


def normalizeImage(image):
    """
    Normalize the image by scaling pixel values to the range [0, 1].

    Parameters:
        image (numpy.ndarray): The input image to be normalized.

    Returns:
        numpy.ndarray: The normalized image.
    """
    # Apply normalization by dividing pixel values by 255
    return image / 255.0


def preprocessImage(image, img_height, img_width):
    """
    Preprocess the image by resizing and normalizing it.

    Parameters:
        image (numpy.ndarray): The input image to be preprocessed.
        img_height (int): The target height for the resized image.
        img_width (int): The target width for the resized image.

    Returns:
        numpy.ndarray: The preprocessed image.
    """
    # Resize the image and then normalize it
    return normalizeImage(ResizeImage(image, img_height, img_width))


def make3dFilter(x):
    """
    Create a 3D filter tuple with the same value repeated three times.

    Parameters:
        x (any): The value to be repeated in the tuple.

    Returns:
        tuple: A tuple with the value repeated three times.
    """
    return tuple([x] * 3)


def make2dFilter(x):
    """
    Create a 2D filter tuple with the same value repeated two times.

    Parameters:
        x (any): The value to be repeated in the tuple.

    Returns:
        tuple: A tuple with the value repeated two times.
    """
    return tuple([x] * 2)


def getBatchData(input_folder_list, output_folder_list, batch_idx, batch_size, imgs_tensor):
    """
    Prepare a batch of data for training/testing.

    Parameters:
        source_path (str): Path to the data directory.
        shuffled_folder_list (list): List of shuffled folder names.
        batch_idx (int): Index of the current batch.
        batch_size (int): Number of samples in each batch.
        imgs_tensor (tuple): Contains dimensions and indices for image processing.
        img_idxs (list): A list of image indices to be read.
        idx (int): the number of image indices 
        folder_idx (int): the number of a folder (a folder is a sequence)
    Returns:
        Tuple of (batch_data, batch_labels)  for a certain batch (eg:id = 2)
    """
    
    [num_imgs,img_height,img_width] = [len(imgs_tensor[0]), imgs_tensor[1], imgs_tensor[2]]
    img_idxs = imgs_tensor[0]  # Assuming this is a list of image indices to be read; IMAGE INDICES, very important

    data_shape = (batch_size, num_imgs, img_height, img_width, 3) # 3 is the number of RGB channels
    batch_data = np.zeros(data_shape, dtype=np.float32) 
    batch_labels = np.zeros(data_shape, dtype=np.float32) 

    # Retrieve the folder names for the current batch from the CSV
    
    for folder_idx in range(batch_size): # a folder is a sequence
        # Load input images
        base_input_idx = folder_idx + (batch_idx * batch_size) 
        input_imgs_path = input_folder_list[base_input_idx]
        label_imgs_path = output_folder_list[base_input_idx]
        
        input_imgs = os.listdir(input_imgs_path)
        label_imgs = os.listdir(label_imgs_path)

        for idx, item in enumerate(img_idxs):

            input_img_path = os.path.join(input_imgs_path, input_imgs[item])
            label_img_path = os.path.join(label_imgs_path, label_imgs[item])
            
            img = imread(input_img_path).astype(np.float32)
            label_img = imread(label_img_path).astype(np.float32)
            for c in range(3): # For RGB channels
                batch_data[folder_idx, idx, :, :, c] = preprocessImage(img[:,:,c], img_height, img_width)
                batch_labels[folder_idx, idx, :, :, c] = preprocessImage(label_img[:,:,c], img_height, img_width)
        # Load label images (assuming similar structure and processing as input images)   
    return batch_data, batch_labels


def generator(source_path, input_folder_list, output_folder_list, batch_size, imgs_tensor):
    """
    for adjust batch size

    Parameters:
      source_path (str): Path to the data directory.
      input_folder_list (list): List of shuffled input folder names.
      output_folder_list (list): List of shuffled outputput folder names.   
      batch_size (int): Number of samples in each batch.
      imgs_tensor (tuple): Contains dimensions and indices for image processing.

    
    Returns:
      check get batch data
    """
    print( 'Source path = ', source_path, '; batch size =', batch_size)
    while True:
        num_batches = int(len(input_folder_list)/batch_size)
        for batch_idx in range(num_batches): #  Iterate over the number of batches
            yield getBatchData(input_folder_list, output_folder_list, batch_idx, batch_size, imgs_tensor)        
        # write the code for the remaining data points which are left after full batches
        # checking if any remaining batches are there or not
        if len(input_folder_list)%batch_size != 0:
            # updated the batch size and yield
            batch_size = len(input_folder_list)%batch_size # take the remainder
            yield getBatchData(input_folder_list, output_folder_list, batch_idx, batch_size, imgs_tensor)
            
def getImgTensor(n_frames):
    """
    Generate a tensor for image data with specified number of frames.

    Parameters:
        n_frames (int): The number of frames to generate indices for.

    Returns:
        list: A list containing the frame indices and the dimensions of the image tensor.
    """
    
    # Generate evenly spaced indices from 0 to 100, rounded to the nearest integer
    img_idx = np.round(np.linspace(0, 100, n_frames)).astype(int)
    
    # Return the list containing the frame indices and the dimensions of the image tensor
    return [img_idx, 60, 80, 3]  # The dimensions are [number of frames, height, width, channels]

# Function to plot model history from a DataFrame
def plotModelHistoryFromFile(history_df, fig_initial_value=1, save_fig=False, file_name=None, fig_vars=None):
    """
    Plots the training and validation history of a model from a DataFrame.

    Parameters:
        history_df (pandas.DataFrame): DataFrame containing the training history.
        fig_initial_value (int): Initial value for the epoch range. Default is 1.
        save_fig (bool): Whether to save the figure to a file. Default is False.
        file_name (str): Name of the file to save the figure. Default is None.
        fig_vars (list of tuples): List of tuples specifying the variables to plot and their titles.
                                   Each tuple should be in the form (train_var, val_var, title). Default is None.

    Returns:
        None
    """
    # Create subplots
    fig, ax = plt.subplots(1, 2, figsize=(15, 4))
    fontsize_label = 12
    
    # Extract keys from DataFrame columns
    keys = history_df.columns
    
    # Default plot variables if not provided
    if fig_vars is None:
        fig_vars = [
            ('loss', 'val_loss', "Train loss vs Validation loss"),
            ('root_mean_squared_error', 'val_root_mean_squared_error', "Train RMSE vs Validation RMSE") # previously, it used MSE
        ]
    
    # Number of epochs (assuming epochs start from fig_initial_value)
    epochs = range(fig_initial_value, fig_initial_value + len(history_df['loss']))
    
    # Iterate over the plot settings and plot each subplot
    for i, (train_var, val_var, title) in enumerate(fig_vars):
        if train_var in keys and val_var in keys:
            # Plot training and validation variables
            ax[i].semilogy(epochs, history_df[train_var], label=train_var)
            ax[i].semilogy(epochs, history_df[val_var], label=val_var)
            ax[i].legend(fontsize=fontsize_label)
            ax[i].set_title(title, fontsize=fontsize_label)
            
            # Additional settings for the subplot
            for spine in ax[i].spines.values():
                spine.set_linewidth(2)
            ax[i].tick_params(direction='in', which='both')
            ax[i].grid(which='both', linestyle='--', linewidth=0.5)
            ax[i].set_xlabel('Epoch', fontsize=fontsize_label)
            ax[i].set_ylabel(ax[i].get_ylabel(), fontsize=fontsize_label)
        else:
            print(f"Warning: {train_var} or {val_var} not found in DataFrame columns.")

    # Adjust layout to ensure subplots do not overlap
    fig.tight_layout()
    plt.show()
    
    # Save the figure if required
    if save_fig:
        if file_name is None:
            # Generate a default file name with a timestamp if none is provided
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'res_{timestamp}.png'
        fig.savefig(file_name, dpi=300)
        print(f"Figure saved as {file_name}")

    # Print max MSE values if available
    if 'loss' in keys and 'val_loss' in keys:
        print("Max. Training MSE:", max(history_df['loss']))
        print("Max. Validation MSE:", max(history_df['val_loss']))
    else:
        print("Warning: 'loss' or 'val_loss' not found in DataFrame columns.")
    
    # Uncomment the following lines to print all history keys and values
    # print("Columns:", keys)
    # for key in keys:
    #     print(f"{key}:", history_df[key].values)

# Function to find the closest scalar value for a given color
def find_closest_scalar(color, df):
    """
    Find the closest scalar value for a given RGB color from a DataFrame.

    Parameters:
        color (tuple or list): The RGB color to find the closest match for. Should be in the form (R, G, B).
        df (pandas.DataFrame): DataFrame containing 'Red', 'Green', 'Blue' columns and corresponding 'Scalar' values.

    Returns:
        float: The scalar value corresponding to the closest RGB color in the DataFrame.
    """
        
    distances = np.linalg.norm(df[['Red', 'Green', 'Blue']].values - np.array(color[:3]), axis=1)
    closest_index = np.argmin(distances)
    return df.loc[closest_index, 'Scalar']

# Encapsulated function
def find_and_plot_closest_scalar(data, scalar_color_map, frame_index=0, roi_size=20, data_batch_size=0, show_image=True):
    """
    Find the closest scalar value for a color in the center ROI of the given frame, and plot the frame.

    Parameters:
        data (numpy.ndarray): The data array containing frames.
        scalar_color_map (pandas.DataFrame): DataFrame containing 'Red', 'Green', 'Blue' columns and corresponding 'Scalar' values.
        frame_index (int): The index of the frame to analyze. Default is 0.
        roi_size (int): The size of the Region of Interest (ROI) centered on the frame. Default is 20.
        data_batch_size (int): The batch size index to select data from. Default is 0.
        show_image (bool): Whether to show the image of the frame. Default is True.


    Returns:
        float: Calculated true value of heat flux.
    """

    # Set the center point (x, y)
    center_x, center_y = data.shape[3] // 2, data.shape[2] // 2

    # Validate ROI size
    if roi_size <= 0 or roi_size > min(center_x, center_y):
        raise ValueError("ROI size must be a positive integer and less than or equal to the half size of the frame dimensions.")

    # Define the ROI (Region of Interest)
    half_size = roi_size // 2
    roi = data[data_batch_size, frame_index, center_y - half_size:center_y + half_size + 1, center_x - half_size:center_x + half_size + 1, :3]

    # Calculate the average color in the ROI
    average_color = np.mean(roi, axis=(0, 1))

    # Normalize the average color if necessary
    if average_color.max() > 1:
        average_color = average_color / 255.0

    # Append alpha value 255 to the average color if necessary
    if len(average_color) == 3:
        average_color = np.append(average_color, 255)

    # Find the closest scalar value for the center color
    closest_scalar = find_closest_scalar(average_color, scalar_color_map)

    print(f"The closest scalar value for the center color {average_color} is {closest_scalar}")

    # Plot the frame
    if show_image:
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(data[data_batch_size, frame_index])
        plt.title(f"Frame {frame_index}")
        plt.axis('off')
        plt.show()

    return closest_scalar


def cal_true_value(heatflux_type, **kwargs):
    """
    Calculate the true value of heat flux based on the specified type.

    Parameters:
        heatflux_type (str): Type of heat flux ('constant' or 'sin').
        kwargs: Additional parameters based on the heatflux_type.

            For 'constant':
                groundtruth_heatflux (list): List of ground truth heat flux values.
                closest_filename_index (int): Index for selecting the ground truth value.
            For 'sin':
                time_point (float): Time point for sine function calculation.
                A (float): Amplitude for sine function.
            

                
    Returns:
        float: Calculated true value of heat flux.
    
    """
    if heatflux_type == 'constant':
        groundtruth_heatflux = kwargs.get('groundtruth_heatflux')
        closest_filename_index = kwargs.get('closest_filename_index', 0)

        if groundtruth_heatflux is None:
            raise ValueError("groundtruth_heatflux must be provided when heatflux_type is 'constant'.")

        # If the heat flux is constant, return the ground truth value directly
        true_value = groundtruth_heatflux[closest_filename_index]

    elif heatflux_type == 'sin':
        time_point = kwargs.get('time_point')
        A = kwargs.get('A')

        if time_point is None or A is None:
            raise ValueError("For 'sin' type, both 'time_point' and 'A' must be provided.")

        # Calculate the true value using the sine function
        true_value = A * np.sin(((np.pi * time_point + 1) / 30) - np.pi / 2) + A

    else:
        raise ValueError("Invalid heatflux_type. Must be 'constant' or 'sin'.")

    return true_value

def calculate_errors_single_frame(prediction, ground_truth, batch_index, frame_index):
    """
    Calculate error metrics for a single frame in a batch of predictions and ground truth data.

    Parameters:
        prediction (numpy.ndarray): The predicted data array.
        ground_truth (numpy.ndarray): The ground truth data array.
        batch_index (int): The index of the batch to analyze.
        frame_index (int): The index of the frame within the batch to analyze.

    Returns:
        tuple: A tuple containing the Mean Squared Error (MSE), Mean Absolute Error (MAE), and Mean Error Percentage (MEP).
    """
    
    # Extract the predicted and ground truth frames for the specified batch and frame indices
    predicted_frame = prediction[batch_index, frame_index]
    ground_truth_frame = ground_truth[batch_index, frame_index]
    
    # Calculate Mean Squared Error (MSE)
    mse = mean_squared_error(ground_truth_frame, predicted_frame)
    
    # Calculate Mean Absolute Error (MAE)
    mae = np.mean(np.abs(ground_truth_frame - predicted_frame))

    # Calculate the ratio of the mean predicted value to the mean ground truth value
    ratio = np.mean(predicted_frame) / np.mean(ground_truth_frame)
    
    # Calculate Mean Error Percentage (MEP)
    me_p = ratio - 1    

    return mse, mae, me_p