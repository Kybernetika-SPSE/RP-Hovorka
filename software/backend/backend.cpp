#include <iostream>
#include <map>
#include <string>
#include <variant>

namespace camera_project {

enum class DeviceMode {
    Preview,
    Menu,
    Capture,
    Playback,
    Sleep,
    Error,
};

struct CameraSettings {
    int iso = 200;
    double aperture = 2.8;
    int shutterSpeedUs = 10000;
};

struct CommandSetIso {
    int value;
};

struct CommandSetAperture {
    double value;
};

struct CommandSetShutterSpeed {
    int value;
};

struct CommandCapture {
};

struct CommandSleep {
};

using Command = std::variant<CommandSetIso, CommandSetAperture, CommandSetShutterSpeed, CommandCapture, CommandSleep>;

class SettingsStore {
public:
    void setIso(int value) {
        settings_.iso = value;
    }

    void setAperture(double value) {
        settings_.aperture = value;
    }

    void setShutterSpeed(int value) {
        settings_.shutterSpeedUs = value;
    }

    const CameraSettings& current() const {
        return settings_;
    }

private:
    CameraSettings settings_{};
};

class CommandBus {
public:
    void send(const Command& command) {
        std::visit([this](const auto& item) {
            handle(item);
        }, command);
    }

    void printState() const {
        std::cout << "[backend] mode=" << modeToString(mode_)
                  << " iso=" << settings_.current().iso
                  << " aperture=" << settings_.current().aperture
                  << " shutter_us=" << settings_.current().shutterSpeedUs << '\n';
    }

private:
    void handle(const CommandSetIso& command) {
        settings_.setIso(command.value);
        std::cout << "[backend] set ISO " << command.value << '\n';
    }

    void handle(const CommandSetAperture& command) {
        settings_.setAperture(command.value);
        std::cout << "[backend] set aperture " << command.value << '\n';
    }

    void handle(const CommandSetShutterSpeed& command) {
        settings_.setShutterSpeed(command.value);
        std::cout << "[backend] set shutter speed " << command.value << " us\n";
    }

    void handle(const CommandCapture&) {
        mode_ = DeviceMode::Capture;
        std::cout << "[backend] capture request\n";
    }

    void handle(const CommandSleep&) {
        mode_ = DeviceMode::Sleep;
        std::cout << "[backend] sleep request\n";
    }

    static std::string modeToString(DeviceMode mode) {
        switch (mode) {
        case DeviceMode::Preview: return "preview";
        case DeviceMode::Menu: return "menu";
        case DeviceMode::Capture: return "capture";
        case DeviceMode::Playback: return "playback";
        case DeviceMode::Sleep: return "sleep";
        case DeviceMode::Error: return "error";
        }
        return "unknown";
    }

    DeviceMode mode_ = DeviceMode::Preview;
    SettingsStore settings_{};
};

class InputRouter {
public:
    Command mapButtonPress(const std::string& buttonName) const {
        if (buttonName == "shutter") {
            return CommandCapture{};
        }
        if (buttonName == "power") {
            return CommandSleep{};
        }
        if (buttonName == "iso_up") {
            return CommandSetIso{400};
        }
        if (buttonName == "aperture_up") {
            return CommandSetAperture{4.0};
        }
        return CommandSetShutterSpeed{8000};
    }
};

}  // namespace camera_project

int main() {
    using namespace camera_project;

    CommandBus bus;
    InputRouter router;

    bus.send(router.mapButtonPress("iso_up"));
    bus.send(router.mapButtonPress("aperture_up"));
    bus.send(router.mapButtonPress("shutter"));
    bus.printState();
    bus.send(router.mapButtonPress("power"));
    bus.printState();

    return 0;
}
