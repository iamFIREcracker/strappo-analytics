include mercurial
include nginx
include redis
include python
include supervisor

Exec {
  path => [ "/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "/bin", ],
}

exec { "add_${user}_to_group_www-data":
  command => "usermod -a -G www-data ${user}",
  unless => "id ${user} | grep www-data",
  require => Package[nginx]
}

nginx::site {'gunicorn':
  config => 'gunicorn',
  appname => $appname,
  appport => $appport,
  servername => $servername,
}

supervisor::gunicorn {'supervisor-gunicorn':
  appname => $appname,
  user => $user,
}
