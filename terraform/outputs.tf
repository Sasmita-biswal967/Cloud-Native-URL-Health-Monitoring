output "public_ip" {
  value = aws_instance.url_monitor_ec2.public_ip
}

output "instance_id" {
  value = aws_instance.url_monitor_ec2.id
}