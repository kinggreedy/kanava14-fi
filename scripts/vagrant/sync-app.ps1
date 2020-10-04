$project = "blog-platform";
$server = "192.168.102.199";
$username = "vagrant";
$password = "vagrant";
$port = "22";
$project_host_dir = "../../app/$project";
$project_guest_dir = "ssh://$server//opt/kanava14fi/$project";

unison -fat -perms 0 -dontchmod -watch -repeat watch -prefer $project_guest_dir -ignore "Path .pytest_cache" -sshargs "-l $username -P $port -pw $password" $project_host_dir $project_guest_dir
