#include <opencv2/opencv.hpp>
#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/image_encodings.h>
#include <string>

int main(int argc, char** argv)
{
  ros::init(argc, argv, "camara");
  ros::NodeHandle nh;

  char* cam_port = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=NV12, framerate=60/1 ! nvvidconv flip-method=2 ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink drop=true"; //flip-method = 2, para voltear la imagen (sino aparece al reves)

  cv::VideoCapture cap(cam_port);

  if (!cap.isOpened())
  {
    ROS_ERROR("No se pudo abrir la webcam");
    return -1;
  }

  ros::Publisher camPub = nh.advertise<sensor_msgs::Image>("/cam", 1);

  cv_bridge::CvImage bridge;

  ros::Rate rate(100);
  while (ros::ok())
  {
    cv::Mat frame;
    cap >> frame;

    if (!frame.empty())
    {
      bridge.header.stamp = ros::Time::now();
      bridge.header.frame_id = "camera_frame";
      bridge.encoding = sensor_msgs::image_encodings::BGR8;
      bridge.image = frame;

      sensor_msgs::ImagePtr img_msg = bridge.toImageMsg();
      camPub.publish(img_msg);
    }

    ros::spinOnce();
    rate.sleep();
  }

  cap.release();

  return 0;
}
