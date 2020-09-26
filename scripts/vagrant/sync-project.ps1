$project = "kanava14-fi";
$server = "192.168.102.199";
$username = "vagrant";
$password = "vagrant";
$port = "10422";
$project_host_dir = "../..";
$project_guest_dir = "ssh://$server//opt/python3test/$project";

unison -fat -perms 0 -dontchmod -watch -repeat watch -prefer $project_guest_dir -ignore "Path app/blog-platform/.pytest_cache" -ignore "Path log" -sshargs "-l $username -P $port -pw $password" $project_host_dir $project_guest_dir
